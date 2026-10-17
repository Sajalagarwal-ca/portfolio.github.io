(function () {
	'use strict';

	var dialog = document.getElementById('project-story-dialog');
	var frame = document.getElementById('project-story-frame');
	var closeButton = document.getElementById('project-story-close');
	if (!dialog || !frame || !closeButton || typeof dialog.showModal !== 'function') return;

	var activeTrigger;
	document.querySelectorAll('[data-project-story]').forEach(function (trigger) {
		trigger.addEventListener('click', function (event) {
			if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
			event.preventDefault();
			activeTrigger = trigger;
			frame.src = trigger.href;
			dialog.showModal();
			document.body.classList.add('has-project-story');
		});
	});

	closeButton.addEventListener('click', function () {
		dialog.close();
	});

	function closeOnEscape(event) {
		if (event.key === 'Escape' && dialog.open) {
			event.preventDefault();
			dialog.close();
		}
	}

	document.addEventListener('keydown', closeOnEscape);
	frame.addEventListener('load', function () {
		if (frame.contentDocument) {
			frame.contentDocument.addEventListener('keydown', closeOnEscape);
		}
	});

	dialog.addEventListener('click', function (event) {
		if (event.target !== dialog) return;
		var bounds = dialog.getBoundingClientRect();
		if (event.clientX < bounds.left || event.clientX > bounds.right ||
			event.clientY < bounds.top || event.clientY > bounds.bottom) {
			dialog.close();
		}
	});

	dialog.addEventListener('close', function () {
		document.body.classList.remove('has-project-story');
		frame.removeAttribute('src');
		if (activeTrigger) activeTrigger.focus();
	});
})();
