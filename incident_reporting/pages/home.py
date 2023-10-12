import dash


dash.register_page(__name__, path="/")

layout = dash.dcc.Markdown(
    """
    # UCPD Incident Tracking

    This project was undertaken with the goal of showing a more granular
        picture of incidents are posted on the
        [UCPD Incident Report](https://incidentreports.uchicago.edu/) page.

        The code for this project is stored in two places:
        - The UCPD incident web-scraper:
            [Link](https://github.com/michplunkett/ucpd-incident-scraper)
        - The Starlit application for data display:
            [Link](https://github.com/michplunkett/ucpd-incident-reporting)

        For more information on this project, or any inquiries related to the
        author, please reach out to me over email at
        **michplunkett[at]gmail[dot]com**.
    """
)
