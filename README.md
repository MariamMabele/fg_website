# Fg Website

`fg_website` is the Frappe app for the Frappe Girls website backend.

It keeps the parts that should be versioned in code:

- Frappe Girls DocTypes
- Web Forms
- Builder page source files
- Builder page sync logic
- website routes and page content

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app fg_website
```

## App structure

The app follows a Builder-first structure:

```text
fg_website/
  hooks.py
  modules.txt
  setup/
    builder_sync.py
  frappe_girls/
    doctype/
    web_form/
    page_source/
      pages/
```

## Builder workflow

The live website is edited in Frappe Builder, but this app keeps the page source copy used to seed Builder.

1. Build and test pages in Frappe Builder and Web Forms.
2. Copy the latest page HTML, head snippet, and data script into `fg_website/frappe_girls/page_source/pages/`.
3. Keep DocTypes and Web Forms in the app updated through normal Frappe export files.
4. Install or migrate the app to sync app-owned Builder pages into the site.

`fg_website.setup.builder_sync` creates and updates Builder Page records from the files in `fg_website/frappe_girls/page_source/pages/`.

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
