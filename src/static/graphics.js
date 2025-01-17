const selectGraphic = document.getElementById('grafico');
const selectGraphicItem = document.getElementById('grafico_item');

const contenedorGraficos = document.getElementById('graficotes');

const url = 'http://127.0.0.1:5000';

let servidores = [];
let selectServer = '';
let selectPrueba = '';

selectGraphic.addEventListener('change', async (event) => {
	const { value } = event.target;

	while (document.getElementById('graficotes').firstChild) {
		document.getElementById('graficotes').removeChild(document.getElementById('graficotes').firstChild); // Elimina el primer hijo
	}

	selectServer = value;

	if (selectServer == '') return;

	if (selectServer == 'all') return consultaGeneral();

	selectGraphicItem.removeAttribute('disabled');

	const ordenes = ['Primera', 'Segunda', 'Tercera'];
	for (let i = 0; i < servidores[value].length; i++) {
		if (selectGraphicItem.childElementCount > 4) selectGraphicItem.removeChild(selectGraphicItem.children[2]);
		const optionCreado = document.createElement('option');
		optionCreado.innerText = `${ordenes[i]}`;
		optionCreado.setAttribute('value', servidores[value][i]);
		selectGraphicItem.appendChild(optionCreado);
	}
});

selectGraphicItem.addEventListener('change', (event) => {
	const { value } = event.target;
	selectPrueba = value;

	if (selectPrueba == '') {
	}
});

window.addEventListener('load', async () => {
	const consulta = await fetch(`${url}/data`);
	const data = await consulta.json();
	servidores = await data;

	for (const el of Object.keys(data)) {
		const optionCreado = document.createElement('option');
		optionCreado.innerText = `${el}`;
		optionCreado.setAttribute('value', el);
		selectGraphic.appendChild(optionCreado);
	}
});

const consultaGeneral = async () => {
	try {
		const consulta = await fetch(`${url}/general`);
		const data = await consulta.json();
		// console.log('data :', data);

		graficoTiempo(data);
		graficoProcessing(data);
		graficoWaiting(data);
	} catch (err) {
		console.log('err :', err);
	} 

const graficoProcessing = (data) => {
	const graficoTiempo = document.createElement('canvas');
	graficoTiempo.setAttribute('id', 'Processing');
	contenedorGraficos.appendChild(graficoTiempo);

	const myLineChart = new Chart(document.getElementById('Processing'), {
		type: 'bar',
		data: {
			labels: [],
			datasets: [],
		},
		options: {
			scales: {
				y: {
					beginAtZero: true,
				},
			},
		},
	});

	myLineChart.data.labels = Object.keys(data);
	myLineChart.data.datasets = [
		{
			label: 'Tiempo Max. Procesamiento',
			data: Object.values(data).map((el) => el.processing_max),
			borderWidth: 1,
		},
		{
			label: 'Tiempo Media Procesamiento',
			data: Object.values(data).map((el) => el.processing_medium),
			borderWidth: 1,
		},
		{
			label: 'Tiempo Min Procesamiento',
			data: Object.values(data).map((el) => el.processing_min),
			borderWidth: 1,
		},
	];

	myLineChart.update();
};

const graficoWaiting = (data) => {
	const graficoWaiting = document.createElement('canvas');
	graficoWaiting.setAttribute('id', 'graficoWaiting');
	contenedorGraficos.appendChild(graficoWaiting);

	const myLineChart = new Chart(document.getElementById('graficoWaiting'), {
		type: 'bar',
		data: {
			labels: [],
			datasets: [],
		},
		options: {
			scales: {
				y: {
					beginAtZero: true,
				},
			},
		},
	});

	myLineChart.data.labels = Object.keys(data);
	myLineChart.data.datasets = [
		{
			label: 'Tiempo Max. Espera',
			data: Object.values(data).map((el) => el.waiting_max),
			borderWidth: 1,
		},
		{
			label: 'Tiempo Media Espera',
			data: Object.values(data).map((el) => el.waiting_medium),
			borderWidth: 1,
		},
		{
			label: 'Tiempo Min Espera',
			data: Object.values(data).map((el) => el.waiting_min),
			borderWidth: 1,
		},
	];

	myLineChart.update();
};
const graficoTiempo = (data) => {
	const graficoTiempo = document.createElement('canvas');
	graficoTiempo.setAttribute('id', 'graficoTiempo');
	contenedorGraficos.appendChild(graficoTiempo);

	const myLineChart = new Chart(document.getElementById('graficoTiempo'), {
		type: 'bar',
		data: {
			labels: [],
			datasets: [],
		},
		options: {
			scales: {
				y: {
					beginAtZero: true,
				},
			},
		},
	});

	myLineChart.data.labels = Object.keys(data);
	myLineChart.data.datasets = [
		{
			label: 'Tiempo Max. Conexión',
			data: Object.values(data).map((el) => el.connect_max),
			borderWidth: 1,
		},
		{
			label: 'Tiempo Media Conexión',
			data: Object.values(data).map((el) => el.connect_medium),
			borderWidth: 1,
		},
		{
			label: 'Tiempo Min Conexión',
			data: Object.values(data).map((el) => el.connect_min),
			borderWidth: 1,
		},
	];

	myLineChart.update();
};
