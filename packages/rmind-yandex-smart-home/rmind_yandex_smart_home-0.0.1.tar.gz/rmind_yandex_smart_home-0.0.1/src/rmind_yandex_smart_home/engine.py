class Engine:
  def handle(event):
    return {
        'request_id': event['headers']['request_id'],
        'payload': {
            'user_id': "f475df023c0e408d8cc84bc79be90017",
            'devices': []
        }
    }