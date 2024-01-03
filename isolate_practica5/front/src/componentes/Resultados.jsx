import React from 'react'
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav'
import Navbar from 'react-bootstrap/Navbar'
import NavDropdown from 'react-bootstrap/NavDropdown'
import Card from 'react-bootstrap/Card';
import './Resultados.css'

function Resultados({productos}) {
    return (
        <Container className="my-gallery">
            {productos.map((producto) => (
                <Card className="my-card">
                    <img src={`img/${producto.image}`} />
                    <Card.Body className="my-card-body">
                        <Card.Title>{producto.title}</Card.Title>
                        <Card.Text>
                            {producto.description}
                        </Card.Text>
                        <p className="price">
                            {producto.price}€
                        </p>
                    </Card.Body>
                </Card>
            ))}
        </Container>
    );
}

export default Resultados;
