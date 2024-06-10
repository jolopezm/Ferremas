import React from 'react';
import ShowInUSD from './ShowInUSD';

export default function Filter({ showInUSD, onShowInUSDChange, categories, onCategoryChange, onSortChange }) {
    const handleCategoryChange = (event) => {
        onCategoryChange(event.target.value);
    };

    const handleSortChange = (event) => {
        onSortChange(event.target.value);
    };

    return (
        <div role="group">
            <details className="dropdown">
                <summary className="summary-small">Región</summary>
                <ul className="summary-small">
                    <li>
                        <ShowInUSD showInUSD={showInUSD} onShowInUSDChange={onShowInUSDChange} />
                    </li>
                </ul>
            </details>
            <details className="dropdown">
                <summary className="summary-small">Categoría</summary>
                <ul className="summary-small">
                    <li>
                        <label>
                            <input
                                type="radio"
                                name="category"
                                value=""
                                onChange={handleCategoryChange}
                            />
                            Todas las categorías
                        </label>
                    </li>
                    {categories.map((category) => (
                        <li key={category.id}>
                            <label>
                                <input
                                    type="radio"
                                    name="category"
                                    value={category.id}
                                    onChange={handleCategoryChange}
                                />
                                {category.nombre}
                            </label>
                        </li>
                    ))}
                </ul>
            </details>
            <details className="dropdown">
                <summary className="summary-small">Ordenar por</summary>
                <ul className="summary-small">
                    <li>
                        <label>
                            <input
                                type="radio"
                                name="sort"
                                value="price-asc"
                                onChange={handleSortChange}
                            />
                            Menor precio
                        </label>
                    </li>
                    <li>
                        <label>
                            <input
                                type="radio"
                                name="sort"
                                value="price-desc"
                                onChange={handleSortChange}
                            />
                            Mayor precio
                        </label>
                    </li>
                </ul>
            </details>
        </div>
    );
}
