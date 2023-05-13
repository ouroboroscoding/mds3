description='MySQL Dump to S3'

epilog = \
"""By using the MDS3 configuration file, normally found in ~/.mds3, we can cut
out a lot of the repetitive work of making backups.

For example we can setup several sections and then call them by name

$: echo '{
  "__default__": {
    "host": "db.mydomain.com",
    "user": "db_user",
    "password": "[redacted]",
    "bucket": "mydomain",
    "zip": true
  },

  "primary": {
    "databases": "primary",
    "key": "backups/primary_|DATETIME|.sql.gz"
  },

  "secondary": {
    "databases": "secondary1 secondary2"
    "key": "backups/secondary_|DATETIME|.sql.gz
  }
}' > ~/.mds3

$: %(prog)s primary

Would then fetch all the data in the `primary` DB of db.mydomain.com and put it
on S3 at mydomain:backups/backups/primary_202305135500.sql.gz

$: %(prog)s primary secondary

Would run each section one at a time, adding both files to S3. Because the host
and bucket names are the same for both, we add them to the __default__ section
there by allowing us to change them only once if need be when the server changes
locatins. The same is true for all variables. Any section requested will first
be set by the values in __default__, then merged with the section itself. The
same is true of anything run from the command line. If we want to ensure that
all backups are zipped by default:

$: echo '{
{
  "__default__": {
    "zip": true
  }
}' > ~/.mds3

$: %(prog)s -d primary -b mydomain

So running the above would fetch the `primary` database off localhost and place
it on the bucket mydomain, but it would be zipped even though not requested.
"""