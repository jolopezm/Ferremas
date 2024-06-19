import React from 'react';

const Payment = ({ url_tbk, token, submit }) => {
  return (
    <form action={url_tbk} method="POST">
      <input type="" name="token_ws" value={token} />
      <button type="submit">{submit}</button>
    </form>
  );
};

export default Payment;
