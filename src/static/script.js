const form = document.querySelector('form');

const loader = document.querySelector('.filtrado');

toastr.options = {
	closeButton: false,
	debug: false,
	newestOnTop: false,
	progressBar: true,
	positionClass: 'toast-top-right',
	preventDuplicates: true,
	onclick: null,
	showDuration: '300',
	hideDuration: '1000',
	timeOut: '5000',
	extendedTimeOut: '1000',
	showEasing: 'swing',
	hideEasing: 'linear',
	showMethod: 'fadeIn',
	hideMethod: 'fadeOut',
};

form.addEventListener('submit', (e) => {
	e.preventDefault();
	const formData = new FormData(form);

	const datos = Object.fromEntries(formData);

	if (!isValidHttpUrl(datos.url)) {
		return toastr.error('No es una url valid', 'Error');
	}

	if (datos.url.split('/').length - 1 < 3) {
		datos.url = `${datos.url}/`;
	}

	loader.classList.toggle('loading');

	fetch('http://127.0.0.1:5000/bechmark', {
		method: 'post',
		body: JSON.stringify(datos),
		headers: {
			'Content-Type': 'application/json',
		},
	})
		.then((resp) => resp.json())
		.then((data) => {
			loader.classList.toggle('loading');

			if (data.code == 'success') {
				toastr.success(data.msg, data.code.toUpperCase());
			}
			console.log(data);
		});
});

let isValidHttpUrl = (string) => {
	let url;

	try {
		url = new URL(string);
	} catch (_) {
		return false;
	}

	return url.protocol === 'http:' || url.protocol === 'https:';
};
