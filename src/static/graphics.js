const ctx = document.getElementById('myChart');
const selectGraphic = document.getElementById('grafico');
const selectGraphicItem = document.getElementById('grafico_item');

const url = 'http://127.0.0.1:5000';

let servidores = [];
let selectServer = '';
let selectPrueba = '';
let datasets = [
	{
		label: '# of Votes',
		data: [12, 19, 3, 5, 2, 3],
		borderWidth: 1,
	},
];
let labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'];
let typeGraphic = 'bar';

const createGraphic = () => {
	ctx.destroy();
	new Chart(ctx, {
		type: typeGraphic,
		data: {
			labels: labels,
			datasets: datasets,
		},
		options: {
			scales: {
				y: {
					beginAtZero: true,
				},
			},
		},
	});
};

selectGraphic.addEventListener('change', async (event) => {
	const { value } = event.target;

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
		console.log(data);
		createGraphic();
	} catch (err) {
		console.log('err :', err);
	} finally {
		console.log('Nuevo gráfico general');
	}
};
