import React from 'react';

export default function Footer() {
    return (
        <footer className="container-fluid">
            <div className="grid">
                <div>
                    <h3>Company Name</h3>
                    <p>Leading provider of construction tools and materials.</p>
                </div>
                <div>
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="#">Home</a></li>
                        <li><a href="#">About Us</a></li>
                        <li><a href="#">Services</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                </div>
                <div>
                    <h3>Contact Us</h3>
                    <p>Email: info@company.com</p>
                    <p>Phone: +1 123 456 7890</p>
                    <p>Address: 1234 Street Name, City, Country</p>
                </div>
                <div>
                    <h3>Follow Us</h3>
                    <ul className="social">
                        <li><a href="#">Facebook</a></li>
                        <li><a href="#">Twitter</a></li>
                        <li><a href="#">LinkedIn</a></li>
                        <li><a href="#">Instagram</a></li>
                    </ul>
                </div>
            </div>
            <div className="text-center">
                <p>&copy; {new Date().getFullYear()} Company Name. All rights reserved.</p>
            </div>
        </footer>
    );
}
