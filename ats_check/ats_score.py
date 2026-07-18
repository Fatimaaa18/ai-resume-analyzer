import pdfplumber


def check_ats_friendliness(pdf_file) -> dict:
    score = 100
    issues = []

    with pdfplumber.open(pdf_file) as pdf:
        total_tables = 0
        total_images = 0
        total_text_length = 0

        for page in pdf.pages:
            tables = page.find_tables()
            total_tables += len(tables)

            total_images += len(page.images)

            page_text = page.extract_text()
            if page_text:
                total_text_length += len(page_text)

        if total_tables > 0:
            score -= 20
            issues.append("Resume contains tables, which can confuse ATS parsers.")

        if total_images > 0:
            score -= 15
            issues.append("Resume contains images/graphics, which ATS systems cannot read.")

        if total_text_length < 200:
            score -= 25
            issues.append("Very little text could be extracted, suggesting complex formatting.")

    score = max(score, 0)

    return {
        "ats_score": score,
        "issues": issues
    }