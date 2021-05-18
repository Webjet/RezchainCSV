# rezchaincsv
A Python package for CSV based Rezchain API

## Install
To install from Github:

```
pip3 install git+https://github.com/Webjet/rezchaincsv -U
```

## Example
Below an actual example of the usage in a Webbeds program.

```python
import rezchaincsv as rz

# The mapping
SH_MAPPING = {
    'BookingID': rz.COMMON_ID,
    'PartnerName': None,
    'BookingStatus': rz.STATUS,
    'PartnerReference': None,
    'AddedDate': rz.Datetime(null=True),
    'CancelDate': rz.Datetime(null=True),
    'LastChanged': rz.LAST_MODIFIED,
    'checkInDate': rz.CHECKIN,
    'checkOutDate': rz.CHECKOUT,
    'Nights': rz.NIGHTS,
    'NumberofRooms': rz.ROOMS,
    'Currency': rz.CURRENCY,
    'OriginalNetAmount': rz.Number(null=0),
    'CurrentNetAmount': rz.AMOUNT,
}

    # ...

    df = get_bookings(query) # We use Pandas to read all bookings
    rezchain = rz.Rezchain(SH_MAPPING)
    for r in df.itertuples(index=False): # Add every row
        rezchain.add_item(r._asdict()) 

    if not args.dry:
        rezchain.to_azure(filename=filename, share_name=AZURE_BLOB_SHARE_NAME, conn_string=conn_string)

    if args.localstore:
        rezchain.to_csv(filename)
```