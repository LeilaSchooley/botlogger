from complete_purchase_flow import CompletePurchaseFlow
import sys

app_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
product = sys.argv[2] if len(sys.argv) > 2 else "google-ads-clicker"

flow = None
try:
    flow = CompletePurchaseFlow(app_url=app_url)
    success = flow.run_complete_flow(product)
    print('\nRUNNER: success=' + str(success))
except Exception as e:
    print('\nRUNNER: Exception while running flow:', e)
    import traceback
    traceback.print_exc()
finally:
    if flow:
        flow.close()
    print('RUNNER: finished')

