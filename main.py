import legendaddyclasses as ldc
import legendaddyfunctions as ldf

print("Legendaddy - TheCustomerFactor exported sales report reader")

Q12022_filename = 'salesreport_Q12022.csv'
Q12023_filename = 'salesreport_Q12023.csv'

Q12022 = ldc.Job('Q12022', Q12022_filename)
Q12022.read()

Q12023 = ldc.Job('Current', Q12023_filename)
Q12023.read()

print('Processed file for Q12022:', Q12022.summary.title)
print('Processed file for Q12023:', Q12023.summary.title)

"""
compare 
"""
prospects = []
for service, invoices in Q12022.details.details.items():
    """Check if this service was offered in 2023"""
    try:
        invoices2023 = Q12023.details.details[service]
    except KeyError:
        """Look back to see which customer sales exist for this service"""
        continue
        
    for invoice in invoices: 
        found = False
        for invoice2023 in invoices2023:
            if invoice['customer'] == invoice2023['customer']:
                found = True
        if not found: 
            prospects.append('"' + service + '","' + invoice['customer'] + '",' + invoice['amount'] + ',"' + invoice['job_date'])

prospects.sort()
print('Writing prospects file...')
with open('prospects.csv', 'w') as f:
    f.write("\n".join(prospect for prospect in prospects))





