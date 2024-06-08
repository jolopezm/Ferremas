// src/components/Payment.js
import React from 'react';

const Payment = ({ url_tbk, token, submit }) => {
  return (
    <form action={url_tbk} method="POST">
      asdasdas
      <input type="hidden" name="token_ws" value={token} />
      <button type="submit">{submit}</button>
    </form>
  );
};

export default Payment;
