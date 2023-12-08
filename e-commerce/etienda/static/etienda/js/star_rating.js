document.addEventListener('DOMContentLoaded', function () {
    const ratingContainers = document.querySelectorAll('.star_rating');

    ratingContainers.forEach(function (ratingContainer) {
        const cardId = ratingContainer.dataset.id;
        drawStars(ratingContainer, cardId);
        // setStarListeners(ratingContainer);
    });

    function drawStars(container, cardId) {
        fetchProductRating(cardId)
            .then(data => {
                const rate = data.rating.rate;
                const stars = calculateStars(rate);

                //si hay estrellas, las borramos
                while (container.firstChild) {
                    container.removeChild(container.firstChild);
                }

                const count = container.nextElementSibling;
                stars.forEach(star => {
                    star.cardId = cardId;
                    const starElement = createStarElement(star);
                    container.appendChild(starElement);
                });
                count.innerHTML = `(${data.rating.count})`;

                setStarListeners(container);
            });
    }

    function setStarListeners(container) {
        const stars = container.querySelectorAll('.rating__star');
        stars.forEach(function (star) {
            star.addEventListener('mouseover', function () {
                const index = star.dataset.index;
                blindStars(container);
                highlightStars(index, container);
            });

            star.addEventListener('mouseout', function () {
                drawStars(container, star.getAttribute('data-card-id'));
            });

            star.addEventListener('mousedown', function() {
                changeColorStars(container, star.getAttribute('data-index'));
            });

            star.addEventListener('click', (event) => {
				const puntuacion = parseInt(event.target.dataset.index) + 1;

				console.log(`La valoración ha sido de: ${puntuacion}`);

				const element_id = star.getAttribute('data-card-id');
                console.log(element_id);
				fetch(`http://0.0.0.0:8000/etienda/api/productos/${element_id}/${puntuacion}`, { method: 'PUT' })
				 	.then(response => response.json())
				 	.then(() => {
				 		drawStars(container, element_id);
				 	})
				 	.catch(error => {
				 		console.error('Error al realizar la solicitud PUT:', error);
				 	});
			});
        });
    }

    async function fetchProductRating(cardId) {
        const response = await fetch(`http://0.0.0.0:8000/etienda/api/productos/${cardId}`);
        return response.json();
    }

    function calculateStars(rate) {
        let fullStars = Math.floor(rate);
        let hasHalfStar = rate % 1 > 0.3 && rate % 1 < 0.8;
        let emptyStars = hasHalfStar ? 4 - fullStars : 5 - fullStars;

        const stars = [];

        for (let i = 0; i < fullStars; i++) {
            stars.push({ className: 'fa-star', cardId: null, index: i });
        }

        if (hasHalfStar) {
            stars.push({ className: 'fa-star-half-o', cardId: null, index: fullStars });
        }

        for (let i = 0; i < emptyStars; i++) {
            stars.push({ className: 'fa-star-o', cardId: null, index: fullStars + (hasHalfStar ? 1 : 0) + i });
        }

        return stars;
    }

    function createStarElement(star) {
        const starElement = document.createElement('span');
        starElement.classList.add('rating__star', 'fa', star.className);
        starElement.setAttribute("data-card-id", star.cardId);
        starElement.setAttribute("data-index", star.index);
        return starElement;
    }

    function blindStars(container) {
        const stars = container.querySelectorAll('.rating__star');
        stars.forEach(function (star) {
            star.classList.remove('fa-star', 'fa-star-half-o');
            star.classList.add('fa-star-o');
        });
    }

    function highlightStars(index, container) {
        const stars = container.querySelectorAll('.rating__star');
        for (let i = 0; i <= index; i++) {
            stars[i].classList.remove('fa-star-o', 'fa-star-half-o');
            stars[i].classList.add('fa-star');
        }
    }

    function changeColorStars(container, index) {
        const stars = container.querySelectorAll('.rating__star');
        for (let i = 0; i <= index; i++) {
            stars[i].classList.add('star_pressed_color');
        }
    }
});