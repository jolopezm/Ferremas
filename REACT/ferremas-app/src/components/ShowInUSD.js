import React from 'react';

export default function ShowInUSD({ showInUSD, onShowInUSDChange }) {
    return (
        <label>
            <input
                type="checkbox"
                checked={showInUSD}
                onChange={onShowInUSDChange}
                
            />
            Mostrar precios en USD
        </label>
    );
}
