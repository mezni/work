from factories import MSISDNFactory



local_msisdn = MSISDNFactory.generate(
    msisdn_type="local",
    country_code="1",
    ndc=234  # Single NDC
)
print(f"Generated Local MSISDN (Default Digits): {local_msisdn}")

# Example for 'international' MSISDN with default digits
international_msisdn = MSISDNFactory.generate(
    msisdn_type="international",
    prefix=["+44", "+1", "+91"]
)
print(f"Generated International MSISDN (Default Digits): {international_msisdn}")