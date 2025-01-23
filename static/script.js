document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        resultContainer.textContent = 'Predicting...';

        const formData = new FormData(form);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.price) {
                resultContainer.textContent = `Predicted House Price: ₹${data.price.toLocaleString()} Lakhs`;
            } else {
                resultContainer.textContent = `Error: ${data.error}`;
            }
        } catch (error) {
            resultContainer.textContent = 'An error occurred while predicting the price.';
            console.error('Error:', error);
        }
    });
});