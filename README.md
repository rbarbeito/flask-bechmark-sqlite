# Benchmark Checker

## Installation

To install and run the Benchmark Checker application, follow these steps:

1. Clone the repository:
```
git clone https://github.com/rbarbeito/flask-bechmark-sqlite
```

2. Navigate to the project directory:
```
cd flask-bechmark-sqlite
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Run the Flask application:
```
python app.py
```

The application will start running on `http://localhost:5000/`.

## Usage

The Benchmark Checker application allows you to perform performance tests on various server configurations, including Nginx, Apache, and Node.js. To use the application, follow these steps:

1. Open your web browser and navigate to `http://localhost:5000/`.
2. Select the server type from the dropdown menu.
3. Enter the URL of the endpoint you want to test.
4. Specify the number of requests and the concurrency level.
5. Click the "Ejecutar test" button to start the benchmark test.

The application will display the results of the test, including the time taken for the tests, the number of complete and failed requests, the requests per second, and the time per request.

## API

The Benchmark Checker application exposes a single API endpoint:

`POST /bechmark`

This endpoint accepts a JSON payload with the following parameters:

- `servicio`: The type of server to test (e.g., "nginx", "apache", "nodejs")
- `url`: The URL of the endpoint to test
- `request`: The number of requests to make
- `concurrency`: The number of concurrent requests to make

The API endpoint returns a JSON response with the following structure:

```json
{
  "code": "success",
  "msg": "Datos guardados satisfactoriamente",
  "data": {
    "consulta": [
      {
        "id": 1,
        "server": "nginx",
        "fecha": "2023-04-18 12:34:56",
        "url": "http://example.com/",
        "solicitudes": 500,
        "concurrency": 10
      }
    ],
    "detalles": [
      {
        "id": 1,
        "software": "nginx",
        "length": 1234,
        "concurrency": 10,
        "time_for_tests": 10.5,
        "complete_request": 495,
        "failed_request": 5,
        "request_per_second": 50.0,
        "time_per_request": 0.2,
        "connect_min": 10,
        "connect_max": 50,
        "connect_medium": 25,
        "processing_min": 5,
        "processing_max": 20,
        "processing_medium": 10,
        "waiting_min": 2,
        "waiting_max": 15,
        "waiting_medium": 5,
        "id_consulta": 1
      }
    ],
    "comportamiento": [
      {
        "id": 1,
        "porcentaje": 10,
        "tiempo_real": 1.5,
        "id_consulta": 1
      },
      {
        "id": 2,
        "porcentaje": 50,
        "tiempo_real": 5.0,
        "id_consulta": 1
      },
      {
        "id": 3,
        "porcentaje": 90,
        "tiempo_real": 9.0,
        "id_consulta": 1
      }
    ]
  }
}
```

## Contributing

If you would like to contribute to the Benchmark Checker project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License

This project is licensed under the [MIT License](LICENSE).





