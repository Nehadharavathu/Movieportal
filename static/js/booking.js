document.addEventListener('DOMContentLoaded', () => {
    const seatContainer = document.getElementById('seat-map-container');
    if (!seatContainer) return;

    const ticketPrice = parseFloat(seatContainer.getAttribute('data-price')) || 0;
    const bookedSeats = JSON.parse(seatContainer.getAttribute('data-booked') || '[]');
    
    const seats = document.querySelectorAll('.seat');
    const selectedSeatsInput = document.getElementById('id_seats');
    const selectedSeatsDisplay = document.getElementById('selected-seats-display');
    const totalPriceDisplay = document.getElementById('total-price-display');
    const ticketCountDisplay = document.getElementById('ticket-count-display');
    const bookButton = document.getElementById('book-button');

    let selectedSeats = [];

    // Initialize booked seats
    seats.forEach(seat => {
        const seatId = seat.getAttribute('data-seat');
        if (bookedSeats.includes(seatId)) {
            seat.classList.add('booked');
        } else {
            // Add click listener only to available seats
            seat.addEventListener('click', () => {
                toggleSeat(seat, seatId);
            });
        }
    });

    function toggleSeat(seatElement, seatId) {
        if (seatElement.classList.contains('booked')) return;

        seatElement.classList.toggle('selected');

        if (seatElement.classList.contains('selected')) {
            selectedSeats.push(seatId);
        } else {
            selectedSeats = selectedSeats.filter(id => id !== seatId);
        }

        // Sort selected seats to keep them ordered (e.g., A1, A2, B3)
        selectedSeats.sort((a, b) => {
            if (a[0] !== b[0]) {
                return a[0].localeCompare(b[0]);
            }
            return parseInt(a.slice(1)) - parseInt(b.slice(1));
        });

        updateUI();
    }

    function updateUI() {
        // Update Hidden Form Input
        if (selectedSeatsInput) {
            selectedSeatsInput.value = selectedSeats.join(',');
        }

        // Update displays
        if (selectedSeatsDisplay) {
            selectedSeatsDisplay.textContent = selectedSeats.length > 0 ? selectedSeats.join(', ') : 'None';
        }

        if (ticketCountDisplay) {
            ticketCountDisplay.textContent = selectedSeats.length;
        }

        if (totalPriceDisplay) {
            const total = selectedSeats.length * ticketPrice;
            totalPriceDisplay.textContent = '$' + total.toFixed(2);
        }

        // Enable/Disable checkout button
        if (bookButton) {
            bookButton.disabled = selectedSeats.length === 0;
        }
    }

    // Initial update
    updateUI();
});
