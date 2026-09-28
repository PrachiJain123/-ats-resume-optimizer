"""Resume and Job Description parsing utilities supporting PDF and plain text formats.

Enforces strict structural preservation:
  - Extracts section headers, experience blocks, and education verbatim.
  - Never renames, rephrases, or invents metadata.
  - Estimates page count for page-budget constraints.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

# ---------------------------------------------------------------------------
# Common section-header patterns (case-insensitive)
# ---------------------------------------------------------------------------
_SECTION_HEADER_PATTERNS: list[re.Pattern] = [
    re.compile(
        r"^(?:SUMMARY|PROFESSIONAL\s+SUMMARY|CAREER\s+SUMMARY|OBJECTIVE|PROFILE"
        r"|SKILLS|TECHNICAL\s+SKILLS|CORE\s+COMPETENCIES|KEY\s+SKILLS|AREAS\s+OF\s+EXPERTISE"
        r"|EXPERIENCE|WORK\s+EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|EMPLOYMENT\s+HISTORY|EMPLOYMENT"
        r"|PROJECTS|KEY\s+PROJECTS|PERSONAL\s+PROJECTS|ACADEMIC\s+PROJECTS"
        r"|EDUCATION|ACADEMIC\s+BACKGROUND|QUALIFICATIONS|CERTIFICATIONS|CERTIFICATES"
        r"|HONORS|AWARDS|ACHIEVEMENTS|PUBLICATIONS|INTERESTS|LANGUAGES"
        r"|VOLUNTEER|LEADERSHIP|ACTIVITIES|REFERENCES"
        r"|ADDITIONAL\s+INFORMATION|ADDITIONAL\s+DETAILS|TRAINING)\s*$",
        re.IGNORECASE,
    ),
]

# Experience-section header keywords
_EXPERIENCE_HEADER_KWS = {
    "experience", "work experience", "professional experience",
    "employment history", "employment", "work history",
}

# Education-section header keywords
_EDUCATION_HEADER_KWS = {
    "education", "academic background", "qualifications",
    "certifications", "certificates", "credentials",
    "education & credentials", "education & certifications",
    "education and credentials",
}

# Lines per page estimate (single-column, 11-12pt, standard margins)
_LINES_PER_PAGE = 48


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ExperienceBlock:
    """A single job/role block extracted verbatim from the resume."""
    title: str = ""          # Job title — verbatim
    company: str = ""        # Company name — verbatim
    dates: str = ""          # Date range — verbatim
    location: str = ""       # Location — verbatim
    header_line: str = ""    # The raw line(s) that contained title/company/dates
    bullets: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "company": self.company,
            "dates": self.dates,
            "location": self.location,
            "header_line": self.header_line,
            "bullets": self.bullets,
        }


@dataclass
class EducationBlock:
    """A single education entry extracted verbatim."""
    degree: str = ""         # Degree title — verbatim
    institution: str = ""    # School/university — verbatim
    dates: str = ""          # Date range — verbatim
    details: list[str] = field(default_factory=list)  # GPA, coursework, etc.

    def to_dict(self) -> dict[str, Any]:
        return {
            "degree": self.degree,
            "institution": self.institution,
            "dates": self.dates,
            "details": self.details,
        }


@dataclass
class ResumeSection:
    """A single section of the resume with its original header text."""
    header: str              # EXACT original header text (e.g. "WORK EXPERIENCE")
    content_lines: list[str] = field(default_factory=list)  # Raw lines under this header
    section_type: str = "other"  # "experience", "education", "skills", "summary", "projects", "other"

    def to_dict(self) -> dict[str, Any]:
        return {
            "header": self.header,
            "section_type": self.section_type,
            "content_lines": self.content_lines,
        }


@dataclass
class ParsedResume:
    """Full structural parse of a resume — all metadata extracted verbatim."""
    raw_text: str
    name: str = ""
    contact_lines: list[str] = field(default_factory=list)
    sections: list[ResumeSection] = field(default_factory=list)
    experiences: list[ExperienceBlock] = field(default_factory=list)
    education: list[EducationBlock] = field(default_factory=list)
    estimated_page_count: int = 1
    total_line_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "contact_lines": self.contact_lines,
            "sections": [s.to_dict() for s in self.sections],
            "experiences": [e.to_dict() for e in self.experiences],
            "education": [e.to_dict() for e in self.education],
            "estimated_page_count": self.estimated_page_count,
            "total_line_count": self.total_line_count,
        }

    def get_all_bullets(self) -> list[str]:
        """Returns all experience bullets from all roles."""
        bullets: list[str] = []
        for exp in self.experiences:
            bullets.extend(exp.bullets)
        return bullets

    def get_section_headers(self) -> list[str]:
        """Returns the list of original section headers in order."""
        return [s.header for s in self.sections]


# ---------------------------------------------------------------------------
# PDF extraction
# ---------------------------------------------------------------------------

def extract_text_from_pdf(pdf_source: str | Path | bytes) -> str:
    """Extracts text content from a PDF file path or bytes using PyMuPDF."""
    if not HAS_FITZ:
        raise ImportError("PyMuPDF is required for PDF parsing. Install with `pip install PyMuPDF`.")

    if isinstance(pdf_source, (str, Path)):
        doc = fitz.open(str(pdf_source))
    elif isinstance(pdf_source, bytes):
        doc = fitz.open(stream=pdf_source, filetype="pdf")
    else:
        raise ValueError("Unsupported pdf_source type. Expected filepath or bytes.")

    text_pages: list[str] = []
    for page in doc:
        page_text = page.get_text("text")
        if page_text:
            text_pages.append(page_text)

    full_text = "\n\n".join(text_pages)
    return clean_text(full_text)


def get_pdf_page_count(pdf_source: str | Path | bytes) -> int:
    """Returns the number of pages in a PDF."""
    if not HAS_FITZ:
        return 1
    if isinstance(pdf_source, (str, Path)):
        doc = fitz.open(str(pdf_source))
    elif isinstance(pdf_source, bytes):
        doc = fitz.open(stream=pdf_source, filetype="pdf")
    else:
        return 1
    return len(doc)


# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """Normalizes whitespace, line breaks, and unicode bullet characters."""
    if not text:
        return ""
    text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219\u25CF\u25CB\u25AA\u25AB]", "\n- ", text)
    text = text.replace("\u00a0", " ").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Section header detection
# ---------------------------------------------------------------------------

def _is_section_header(line: str) -> bool:
    """Check if a line is a section header."""
    stripped = line.strip()
    if not stripped or len(stripped) > 60:
        return False
    # Remove trailing colons for matching
    test = stripped.rstrip(":").strip()
    for pattern in _SECTION_HEADER_PATTERNS:
        if pattern.match(test):
            return True
    # Also check for ALL-CAPS lines that look like headers (2-4 words, no digits)
    if test.isupper() and 1 <= len(test.split()) <= 5 and not re.search(r"\d", test):
        return True
    return False


def _classify_section(header: str) -> str:
    """Classify a section header into a type."""
    h_lower = header.strip().rstrip(":").strip().lower()
    if h_lower in _EXPERIENCE_HEADER_KWS or "experience" in h_lower or "employment" in h_lower:
        return "experience"
    if h_lower in _EDUCATION_HEADER_KWS or "education" in h_lower or "certif" in h_lower:
        return "education"
    if "skill" in h_lower or "competenc" in h_lower or "expertise" in h_lower or "technologies" in h_lower:
        return "skills"
    if "summary" in h_lower or "objective" in h_lower or "profile" in h_lower:
        return "summary"
    if "project" in h_lower:
        return "projects"
    return "other"


# ---------------------------------------------------------------------------
# Experience block parsing
# ---------------------------------------------------------------------------

# Date pattern: catches "2022 – Present", "Jan 2020 - Dec 2021", "2019-2022", etc.
_DATE_PATTERN = re.compile(
    r"(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
    r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+)?"
    r"\d{4}\s*(?:[-–—~to]+\s*(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
    r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+)?"
    r"(?:\d{4}|[Pp]resent|[Cc]urrent|[Nn]ow))?",
    re.IGNORECASE,
)


def _parse_experience_blocks(lines: list[str]) -> list[ExperienceBlock]:
    """Parse experience section lines into structured blocks.
    
    Heuristic: Lines containing date ranges are role headers.
    Lines starting with bullet markers are bullets.
    """
    blocks: list[ExperienceBlock] = []
    current_block: ExperienceBlock | None = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check if this line contains a date range (role/company header)
        date_match = _DATE_PATTERN.search(stripped)
        is_bullet = bool(re.match(r"^[-*•–—]\s+|^\d+[.)]\s+", stripped))

        if date_match and not is_bullet and len(stripped) > 8:
            # Save previous block
            if current_block:
                blocks.append(current_block)

            current_block = ExperienceBlock()
            current_block.header_line = stripped
            current_block.dates = date_match.group(0).strip()

            # Try to extract title and company
            # Common formats:
            #   "Job Title | Company | Dates"
            #   "Job Title, Company, Dates"
            #   "Job Title at Company Dates"
            #   "Company — Job Title — Dates"
            remaining = stripped[:date_match.start()].strip().rstrip("|,–—-").strip()
            if remaining:
                # Split on common delimiters
                parts = re.split(r"\s*[|–—]\s*|\s*,\s*", remaining)
                parts = [p.strip() for p in parts if p.strip()]
                if len(parts) >= 2:
                    current_block.title = parts[0]
                    current_block.company = parts[1]
                elif len(parts) == 1:
                    current_block.title = parts[0]
            continue

        # Check for a continuation header line (company on next line, no date)
        if current_block and not current_block.company and not is_bullet and not _is_section_header(stripped):
            if len(stripped) < 80 and not stripped.startswith(("Developed", "Built", "Led", "Managed")):
                current_block.company = stripped
                continue

        if is_bullet and current_block:
            clean_bullet = re.sub(r"^[-*•–—]\s+|^\d+[.)]\s+", "", stripped).strip()
            if len(clean_bullet) > 15:
                current_block.bullets.append(clean_bullet)
        elif current_block and not is_bullet:
            # Could be a continuation of previous bullet or a non-bullet line
            # Check if it starts with an action verb (heuristic for unlabeled bullets)
            action_match = re.match(
                r"^(?:Developed|Designed|Built|Engineered|Spearheaded|Optimized|"
                r"Implemented|Automated|Led|Created|Managed|Analyzed|Reduced|"
                r"Increased|Achieved|Deployed|Architected|Streamlined|Collaborated|"
                r"Conducted|Delivered|Established|Improved|Introduced|Maintained|"
                r"Migrated|Orchestrated|Pioneered|Refactored|Scaled|Transformed)\b",
                stripped, re.IGNORECASE
            )
            if action_match and len(stripped) > 25:
                current_block.bullets.append(stripped)

    if current_block:
        blocks.append(current_block)

    return blocks


def _parse_education_blocks(lines: list[str]) -> list[EducationBlock]:
    """Parse education section lines into structured blocks."""
    blocks: list[EducationBlock] = []
    current: EducationBlock | None = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        is_bullet = bool(re.match(r"^[-*•–—]\s+", stripped))

        # Check for date — indicates new education entry
        date_match = _DATE_PATTERN.search(stripped)

        if date_match and not is_bullet:
            if current:
                blocks.append(current)
            current = EducationBlock()
            current.dates = date_match.group(0).strip()
            remaining = stripped[:date_match.start()].strip().rstrip("|,–—-").strip()
            if remaining:
                parts = re.split(r"\s*[|–—]\s*|\s*,\s*", remaining)
                parts = [p.strip() for p in parts if p.strip()]
                if len(parts) >= 2:
                    current.degree = parts[0]
                    current.institution = parts[1]
                elif len(parts) == 1:
                    current.degree = parts[0]
        elif is_bullet:
            clean = re.sub(r"^[-*•–—]\s+", "", stripped).strip()
            if current:
                current.details.append(clean)
            else:
                # Standalone bullet before any date-bearing line
                current = EducationBlock(degree=clean)
        elif not is_bullet and stripped:
            if current and not current.institution:
                current.institution = stripped
            elif current:
                current.details.append(stripped)
            else:
                # First line, no date — treat as degree
                current = EducationBlock(degree=stripped)

    if current:
        blocks.append(current)

    return blocks


# ---------------------------------------------------------------------------
# Main structural parser
# ---------------------------------------------------------------------------

def parse_resume_full(resume_text: str) -> ParsedResume:
    """Parses a resume into a fully structured representation.
    
    All metadata (name, headers, companies, titles, dates, education) is
    extracted VERBATIM — never renamed, rephrased, or invented.
    """
    lines = resume_text.split("\n")
    total_lines = len([ln for ln in lines if ln.strip()])
    estimated_pages = max(1, (total_lines + _LINES_PER_PAGE - 1) // _LINES_PER_PAGE)

    parsed = ParsedResume(
        raw_text=resume_text,
        total_line_count=total_lines,
        estimated_page_count=estimated_pages,
    )

    # --- Extract name & contact ---
    non_empty = [ln.strip() for ln in lines if ln.strip()]
    if non_empty:
        parsed.name = non_empty[0]

    # Gather contact lines (lines containing email, phone, linkedin, etc.)
    for ln in non_empty[1:4]:  # Check lines 2-4
        if any(kw in ln.lower() for kw in ["@", "phone", "+", "linkedin", "github", "|", "http", "www"]):
            parsed.contact_lines.append(ln)
        else:
            break

    # --- Split into sections ---
    current_section: ResumeSection | None = None
    header_start_idx = len(parsed.contact_lines) + 1  # Skip name + contact lines

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip name and contact lines at the top
        if i < header_start_idx and not _is_section_header(stripped):
            continue

        if _is_section_header(stripped):
            if current_section:
                parsed.sections.append(current_section)
            sec_type = _classify_section(stripped)
            current_section = ResumeSection(
                header=stripped,
                section_type=sec_type,
            )
        elif current_section:
            current_section.content_lines.append(line)
        # Lines before the first section header (after name/contact) are treated as summary
        elif stripped and i >= header_start_idx:
            current_section = ResumeSection(
                header="",
                section_type="preamble",
            )
            current_section.content_lines.append(line)

    if current_section:
        parsed.sections.append(current_section)

    # --- Parse experience and education blocks from their sections ---
    for section in parsed.sections:
        if section.section_type == "experience":
            parsed.experiences.extend(_parse_experience_blocks(section.content_lines))
        elif section.section_type == "education":
            parsed.education.extend(_parse_education_blocks(section.content_lines))

    return parsed


# ---------------------------------------------------------------------------
# Legacy API (backward-compatible)
# ---------------------------------------------------------------------------

def extract_bullet_points(text: str) -> list[str]:
    """Extracts individual experience bullet points from resume text."""
    parsed = parse_resume_full(text)
    bullets = parsed.get_all_bullets()
    if bullets:
        return bullets

    # Fallback: simple line-based extraction
    lines = text.split("\n")
    extracted: list[str] = []
    current_bullet: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_bullet:
                extracted.append(" ".join(current_bullet))
                current_bullet = []
            continue

        is_bullet_start = bool(re.match(r"^[-*•–—]\s+|^\d+[.)]\s+", stripped))
        action_verb_match = bool(re.match(
            r"^(developed|designed|built|engineered|spearheaded|optimized|implemented|"
            r"automated|led|created|managed|analyzed|reduced|increased|achieved|deployed|"
            r"architected|streamlined)\b", stripped, re.IGNORECASE
        ))

        if is_bullet_start:
            if current_bullet:
                extracted.append(" ".join(current_bullet))
            clean_item = re.sub(r"^[-*•–—]\s+|^\d+[.)]\s+", "", stripped)
            current_bullet = [clean_item]
        elif action_verb_match and len(stripped) > 25 and not stripped.endswith(":"):
            if current_bullet:
                extracted.append(" ".join(current_bullet))
            current_bullet = [stripped]
        elif current_bullet:
            current_bullet.append(stripped)

    if current_bullet:
        extracted.append(" ".join(current_bullet))

    # Filter noise
    return [b.strip() for b in extracted
            if len(b.strip()) >= 20
            and not b.strip().lower().startswith(("phone", "email", "linkedin", "github", "address"))]


def parse_resume_structure(resume_text: str) -> dict[str, Any]:
    """Segment resume text into logical sections (legacy API)."""
    parsed = parse_resume_full(resume_text)
    return {
        "raw_text": resume_text,
        "name": parsed.name,
        "contact_info": parsed.contact_lines,
        "summary": "",
        "skills_raw": "",
        "experience_bullets": parsed.get_all_bullets(),
        "parsed": parsed,
    }
