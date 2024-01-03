import React from 'react'
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav'
import Navbar from 'react-bootstrap/Navbar'
import NavDropdown from 'react-bootstrap/NavDropdown'
import './Navegacion.css'

function Navegacion({categorias , filtro}) {
    return (
        <Navbar expand="lg">
        <Container fluid>
            <Navbar.Brand href="#">Store </Navbar.Brand>
            <Navbar.Toggle aria-controls="navbarScroll" />
            <Navbar.Collapse id="navbarScroll">
                <Nav className="me-auto my-2 my-lg-0" style={{ maxHeight: '100px' }} navbarScroll >
                    <NavDropdown title="Categorias" id="navbarScrollingDropdown">
                       {categorias.map((categoria) => (
                            <NavDropdown.Item key={categoria} onClick={() => filtro(categoria)}>{categoria}</NavDropdown.Item>
                        ))}
                    </NavDropdown>
                </Nav>
                <Form className="d-flex">
                    <Form.Control
                        type="search"
                        placeholder="Search"
                        className="me-2"
                        aria-label="Search"
                        onChange={ (evento) => {filtro(evento)}}
                    />
                    <Button>Search</Button>
                </Form>
            </Navbar.Collapse>
        </Container>
    </Navbar>
                
    );
}

export default Navegacion;
