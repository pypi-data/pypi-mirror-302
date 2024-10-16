## Installation
```bash
pip install radifox-qa
```

## Quality Assurance
The web-based quality assurance system is a system for viewing images and recording QA results.
It is a Flask-based webapp that can be run locally.
There are two modes: `conversion` and `processing` that can be switched between using the links in the top navigation bar.

The `conversion` mode is used to view and make corrections to the naming of images after conversion.
There are three types of actions that can be taken in `conversion` mode.
- Ignore Button: This will mark the image to be skipped by the conversion process on update.
- Body Type Buttons: This will change the `bodypart` of the image to the selected value. It is currently available for `BRAIN`, `CSPINE`, `TSPINE`, `LSPINE`, and `ORBITS`.
- Correct Name Button: This will open a form to correct any of the **core** aspects of the RADIFOX naming convention. `extras` are not yet supported.

The `processing` mode is used to view outputs of various processing steps.
For each processing step, images of the outputs are shown with the provenance record for that step.
No actions are currently availabe in `processing` mode, but we hope to record QA results directly from the app.

The QA webapp is launched with the `radifox-qa` command.
It is a webapp that runs locally on port 5000 by default.
Be sure to copy down the Secret Key that is printed to the console when the webapp is launched.
This will be required to log into the webapp and changes each time the app is launched.
It can also be specified using the `--secret-key` option.
For convenience, you can log into the app using `http://{HOST}:{PORT}/login?key={SECRET_KEY}`, which is printed when the app is launched.
It can also be accessed at `http://{HOST}:{PORT}` (`http://localhost:5000` by default) and the key can be entered there.

## Usage
The `radifox-qa` script is used to run the web-based quality assurance system.

Example Usage:
```bash
radifox-qa --port 8888 --root-directory /path/to/output
```
This will launch the QA webapp on port 8888, pointing to `/path/to/output`.
The QA webapp will be accessible at `http://localhost:8888` and will show projects in `/path/to/output`.
Be sure to note the secret key printed to the terminal when the app starts.
You will need this to log into the webapp.
The secret key changes each time the app is launched.

You can specify your own secret key using the `--secret-key` option.

```bash
radifox-qa --port 8888 --root-directory /path/to/output --secret-key my-secret-key
```

## Advanced CLI Usage

### `radifox-qa`
| Option             | Description                                                          | Default     |
|--------------------|----------------------------------------------------------------------|-------------|
| `--port`           | The port to run the QA webapp on.                                    | `5000`      |
| `--host`           | The host bind address for the QA webapp.                             | `localhost` |
| `--root-directory` | The output root to read projects from (contains project directories) | `/data`     |
| `--secret-key`     | The secret key to use for the QA webapp.                             | `None`      |
| `--workers`        | Number of workers to use for web server.                             | `1`         |