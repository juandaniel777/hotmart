# hotmart
Cart abandonment event.
A Webhook is sent from Hotmart in JSON format, after that you have to create a contact in ManyChat and finally set some Fields. This webhook has gspread as a database, a Google service that allows you to use a sheet as a relational database, said service can be consumed with creds.
json said key is shared in the sheet in google drive, data such as the first and last name of the people who abandon the shopping cart, are selected thanks to the splitname.py function.
documentation: https://developers.hotmart.com/docs/es/2.0.0/webhook/cart-abandonment-webhook
