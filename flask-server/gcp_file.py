import webbrowser

service_account_email = 'vidya-801@focal-healer-417403.iam.gserviceaccount.com'
url = f'https://console.cloud.google.com/iam-admin/serviceaccounts/details/{service_account_email}?project=your-project-id'
webbrowser.open(url)