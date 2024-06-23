import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

export const numberWithPoints = (number) => {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
};

export const initTransaction = async (data) => {
    const response = await fetch('http://localhost:8000/api/init-transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    return response.json();
};

export const commitTransaction = async (token) => {
    try {
        const response = await api.post(`/confirm-transaction/${token}`);
        return response
    } catch (error) {
        throw new Error(`Error confirmando la transaccion: ${error.message}`);
    }
}

export const createTransaction = async (token) => {
    try {
        const response = await api.post(`/transaccion/${token}`);
        return response.data;
    } catch (error) {
        throw new Error(`Error creating transaction: ${error.message}`);
    }
};

export const searchTransactionToken = async (token) => {
    try {
        const response = await api.get(`/transaccion/${token}`);
        return response.data;
    } catch (error) {
        throw new Error(`Error fetching transactions: ${error.message}`);
    }
};

export const createOrder = async (data) => {
    try {
        const response = await api.post('/ordenes/', data);
        return response.data;
    } catch (error) {
        console.error('Error in createOrder:', error.response?.data.detail);
        throw error;
    }
};

export const createOrderDetail = async (data) => {
    try {
        const response = await api.post('/detalles_ordenes/', data);
        return response.data;
    } catch (error) {
        throw new Error(`Error creating order detail: ${error.message}`);
    }
};


export const checkOrderCodeExists = async (code) => {
    try {
        const response = await api.get(`/api/check-order-code/${code}`);
        return response.data.exists;
    } catch (error) {
        console.error('Error checking order code:', error);
        throw new Error(`Error checking order code: ${error.message}`);
    }
};

export default api;
