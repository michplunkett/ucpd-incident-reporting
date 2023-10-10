from incident_reporting.external.google_nbd import GoogleNBD


# Just here for testing
if __name__ == "__main__":
    client = GoogleNBD()
    df, incidents = client.get_all_incidents()
