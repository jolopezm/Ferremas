import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

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
}

export default api;
