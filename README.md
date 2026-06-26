# Fg Website

Frappe app for the Frappe Girls website backend and content structure.

This app is currently being used as the source-of-truth repo for:

- Frappe Builder page bodies
- Frappe Builder data scripts
- Web Form field definitions
- DocType field definitions
- website content notes and public copy

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app fg_website
```

## Builder export structure

The main working files for the current site live in `builder_exports/`.

```text
builder_exports/
  pages/
    home/
      body.html
      data_script.py
    events/
      body.html
      data_script.py
    contribute/
      body.html
    organize/
      body.html
    coach/
      body.html
    sponsors/
      body.html
    code_of_conduct/
      body.html
  webforms/
    workshop_application.md
    organizer_request.md
    coach_interest.md
    sponsor_interest.md
  doctypes/
    workshop_event.md
    workshop_application.md
    organizer_request.md
    coach_interest.md
    sponsor_interest.md
    sponsor_profile.md
    event_sponsorship.md
```

## Current workflow

1. Build and test in Frappe Builder / Web Forms on Frappe Cloud.
2. Copy the live page body and data script into this repo.
3. Keep DocType and Web Form definitions updated here.
4. Push changes to GitHub so the website structure is versioned.

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/fg_website
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

## License

mit
