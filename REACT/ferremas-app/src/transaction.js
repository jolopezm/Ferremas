// transaction.js

import { getTransaction } from './api';

export const initTransaction = async (baseurl) => {
  const buy_order = Math.floor(Math.random() * 900000) + 100000;
  const session_id = Math.floor(Math.random() * 900000) + 100000;
  const amount = 15000;
  const return_url = `${baseurl}?action=getResult`;
  const type = 'sandbox';

  const data = {
    buy_order,
    session_id,
    amount,
    return_url,
  };

  const endpoint = '/rswebpaytransaction/api/webpay/v1.0/transactions';
  return await getTransaction(data, 'POST', type, endpoint);
};
