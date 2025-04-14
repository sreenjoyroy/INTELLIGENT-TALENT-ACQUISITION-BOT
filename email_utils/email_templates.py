def hr_confirmation_email(hr_name, applicant_name, applicant_email, position, interview_time):
    return f"""
Hello {hr_name},

An applicant named {applicant_name} ({applicant_email}) has been shortlisted for the position of {position}.

Please confirm if you're available for the interview scheduled at:
📅 {interview_time}

Reply to this email to confirm or reject the schedule.

Thank you,
Talent Acquisition Assistant Bot
"""

def applicant_confirmation_email(applicant_name, position, interview_time):
    return f"""
Hello {applicant_name},

Congratulations! 🎉

You’ve been shortlisted for the position of {position}.
The interview is scheduled at:
📅 {interview_time}

Please be available on time.

Best regards,
Talent Acquisition Assistant Bot
"""

def rejection_email(applicant_name, position):
    return f"""
Hi {applicant_name},

Thank you for your interest in the position of {position}.

After reviewing your resume, we regret to inform you that you do not meet the eligibility criteria for this role.

We wish you all the best in your future endeavors!

Kind regards,
Talent Acquisition Assistant Bot
"""
