# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of this project seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **Do not** open a public issue for security vulnerabilities
2. Email the project maintainers at the email address listed in the repository
3. Provide a detailed description of the vulnerability
4. Include steps to reproduce the issue
5. Allow reasonable time for us to investigate and fix the issue

### What to Expect

- Acknowledgment of your report within 48 hours
- Regular updates on the progress of the fix
- Credit in the security advisory (if desired)
- A patched release within a reasonable timeframe

## Security Best Practices

### Data Privacy

- This project processes crime data from the City of Chicago Data Portal
- The data is publicly available and anonymized
- No personal user data is collected or stored

### Dependencies

- Keep dependencies updated to avoid known vulnerabilities
- Use `pip-audit` to check for vulnerable packages:
  ```bash
  pip install pip-audit
  pip-audit
  ```

### Environment Variables

- Never commit `.env` files to the repository
- Use `.env.example` as a template for environment configuration
- Review environment variables before deployment

### Docker Security

- Use specific image tags (not `latest`)
- Regularly update base images
- Run containers as non-root users when possible
- Use Docker secrets for sensitive data

## Security Checklist for Contributors

- [ ] No hardcoded credentials or API keys
- [ ] Dependencies are from trusted sources
- [ ] Input validation for all user inputs
- [ ] Proper error handling without exposing sensitive information
- [ ] No debug mode enabled in production
- [ ] Environment variables used for configuration

## Contact

For security concerns, please contact the project maintainers through GitHub's security advisory feature or email.