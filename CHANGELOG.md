# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - UNRELEASED

- Nothing yet

## [0.2.0] - 2026-05-08

- Add Django 5.2 and 6.0 support.
- Drop support for Django 4.2, 5.0 and 5.1.
- Drop support for Python 3.9.
- Update dependencies to require Django 5.2 or higher.
- Add compatibility with django-tables2 3.0+
- **BREAKING:** `label` argument of `TableSelectHelper` is renamed `label_field` and now accepts a callable that takes a table row object and returns a string, or a string representing the name of the field to use as the label.

## [0.1.0] - 2024-06-10

- Initial release.
