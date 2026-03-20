from flask import Flask, request, redirect, session, send_file
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'sgru_unmsm_2025'

# Configuración SQLite simple
def init_db():
    conn = sqlite3.connect('sgru.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            codigo TEXT UNIQUE,
            password TEXT,
            rol TEXT,
            nombres TEXT
        )
    ''')
    
    # Insertar usuarios de prueba si no existen
    cursor = conn.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        usuarios = [
            ('20210001', 'sanmarcos123', 'RESIDENTE', 'María González'),
            ('ADMIN001', 'sanmarcos123', 'ADMINISTRATIVO', 'Ana Rodríguez'),
            ('20210002', 'sanmarcos123', 'POSTULANTE', 'Carlos Mendoza'),
            ('TSOCIAL01', 'sanmarcos123', 'TRABAJADOR_SOCIAL', 'Elena Ruiz')
        ]
        
        for codigo, password, rol, nombres in usuarios:
            conn.execute(
                "INSERT INTO usuarios (codigo, password, rol, nombres) VALUES (?, ?, ?, ?)",
                (codigo, password, rol, nombres)
            )
    
    conn.commit()
    conn.close()

# Página principal (index.html original)
@app.route('/')
def pagina_principal():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SGRU - Sistema de Gestión de Residencia Universitaria</title>
        <style>
            :root {
                --primary-color: #003366;
                --secondary-color: #990000;
                --accent-color: #0066cc;
                --light-color: #f5f5f5;
                --dark-color: #333333;
                --success-color: #28a745;
                --warning-color: #ffc107;
                --danger-color: #dc3545;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            body {
                background-color: #f8f9fa;
                color: var(--dark-color);
                line-height: 1.6;
            }
            
            /* Header Styles */
            header {
                background: linear-gradient(135deg, var(--primary-color), #004080);
                color: white;
                padding: 1rem 0;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            
            .header-container {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0 20px;
            }
            
            .logo-container {
                display: flex;
                align-items: center;
                gap: 20px;
            }
            
            .logo {
                width: 80px;
                height: 80px;
                border-radius: 8px;
                object-fit: contain;
                background: white;
                padding: 5px;
            }
            
            .logo-text h1 {
                font-size: 1.5rem;
                margin-bottom: 5px;
                font-weight: 600;
            }
            
            .logo-text p {
                font-size: 0.9rem;
                opacity: 0.9;
            }
            
            .auth-buttons {
                display: flex;
                gap: 15px;
            }
            
            .btn {
                padding: 10px 25px;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
                text-align: center;
            }
            
            .btn-primary {
                background: var(--accent-color);
                color: white;
            }
            
            .btn-primary:hover {
                background: #0044cc;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 102, 204, 0.3);
            }
            
            .btn-outline {
                background: transparent;
                color: white;
                border: 2px solid white;
            }
            
            .btn-outline:hover {
                background: white;
                color: var(--primary-color);
            }
            
            /* Navigation */
            nav {
                background: white;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                position: sticky;
                top: 0;
                z-index: 100;
            }
            
            .nav-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
            }
            
            .nav-menu {
                display: flex;
                list-style: none;
                gap: 30px;
            }
            
            .nav-menu a {
                text-decoration: none;
                color: var(--dark-color);
                font-weight: 500;
                padding: 15px 0;
                display: block;
                transition: color 0.3s ease;
                position: relative;
            }
            
            .nav-menu a:hover {
                color: var(--accent-color);
            }
            
            .nav-menu a::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 0;
                height: 3px;
                background: var(--accent-color);
                transition: width 0.3s ease;
            }
            
            .nav-menu a:hover::after {
                width: 100%;
            }
            
            /* Hero Section */
            .hero {
                background: linear-gradient(rgba(0, 51, 102, 0.8), rgba(0, 51, 102, 0.9)), url('UNMSM.jpg');
                background-size: cover;
                background-position: center;
                color: white;
                padding: 100px 0;
                text-align: center;
            }
            
            .hero-content {
                max-width: 800px;
                margin: 0 auto;
                padding: 0 20px;
            }
            
            .hero h2 {
                font-size: 3rem;
                margin-bottom: 1.5rem;
                font-weight: 700;
            }
            
            .hero p {
                font-size: 1.3rem;
                margin-bottom: 2.5rem;
                opacity: 0.9;
            }
            
            .hero-buttons {
                display: flex;
                gap: 20px;
                justify-content: center;
            }
            
            /* Main Content */
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 60px 20px;
            }
            
            .section-title {
                text-align: center;
                font-size: 2.5rem;
                margin-bottom: 3rem;
                color: var(--primary-color);
                font-weight: 700;
            }
            
            /* Features Section */
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 30px;
                margin-bottom: 60px;
            }
            
            .feature-card {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
            }
            
            .feature-icon {
                font-size: 3rem;
                margin-bottom: 20px;
            }
            
            .feature-card h3 {
                font-size: 1.5rem;
                margin-bottom: 15px;
                color: var(--primary-color);
            }
            
            .feature-card p {
                color: #666;
                line-height: 1.6;
            }
            
            /* Process Section */
            .process-steps {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 30px;
                margin-bottom: 60px;
            }
            
            .step {
                text-align: center;
                padding: 30px 20px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                position: relative;
            }
            
            .step-number {
                width: 50px;
                height: 50px;
                background: var(--accent-color);
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                font-weight: bold;
                margin: 0 auto 20px;
            }
            
            .step h3 {
                margin-bottom: 15px;
                color: var(--primary-color);
            }
            
            .step p {
                color: #666;
                line-height: 1.6;
            }
            
            /* Stats Section */
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 30px;
                margin-bottom: 60px;
            }
            
            .stat-card {
                text-align: center;
                padding: 30px 20px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            
            .stat-number {
                font-size: 3rem;
                font-weight: bold;
                color: var(--accent-color);
                margin-bottom: 10px;
            }
            
            .stat-card p {
                color: #666;
                font-weight: 500;
            }
            
            /* News Section */
            .news-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 30px;
            }
            
            .news-card {
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }
            
            .news-card:hover {
                transform: translateY(-5px);
            }
            
            .news-image {
                height: 200px;
                background-size: cover;
                background-position: center;
                background-color: #ddd;
            }
            
            .news-content {
                padding: 25px;
            }
            
            .news-date {
                color: var(--accent-color);
                font-weight: 500;
                margin-bottom: 10px;
                font-size: 0.9rem;
            }
            
            .news-content h3 {
                margin-bottom: 15px;
                color: var(--primary-color);
                font-size: 1.3rem;
            }
            
            .news-content p {
                color: #666;
                line-height: 1.6;
                margin-bottom: 15px;
            }
            
            /* Footer */
            footer {
                background: var(--primary-color);
                color: white;
                padding: 50px 0 0;
            }
            
            .footer-content {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 40px;
            }
            
            .footer-section h3 {
                margin-bottom: 20px;
                font-size: 1.3rem;
            }
            
            .contact-info {
                list-style: none;
            }
            
            .contact-info li {
                margin-bottom: 15px;
                display: flex;
                align-items: flex-start;
                gap: 10px;
            }
            
            .contact-info i {
                font-style: normal;
                width: 20px;
            }
            
            .footer-links {
                list-style: none;
            }
            
            .footer-links li {
                margin-bottom: 10px;
            }
            
            .footer-links a {
                color: #ccc;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .footer-links a:hover {
                color: white;
            }
            
            .copyright {
                text-align: center;
                padding: 20px;
                margin-top: 50px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                color: #ccc;
                font-size: 0.9rem;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .header-container {
                    flex-direction: column;
                    gap: 20px;
                }
                
                .nav-menu {
                    flex-direction: column;
                    gap: 0;
                }
                
                .hero h2 {
                    font-size: 2rem;
                }
                
                .hero p {
                    font-size: 1.1rem;
                }
                
                .hero-buttons {
                    flex-direction: column;
                    align-items: center;
                }
                
                .features {
                    grid-template-columns: 1fr;
                }
                
                .section-title {
                    font-size: 2rem;
                }
            }
        </style>
    </head>
    <body>
        <!-- Header -->
        <header>
            <div class="header-container">
                <div class="logo-container">
                    <img src="OGBU.png" alt="Logo UNMSM" class="logo">
                    <div class="logo-text">
                        <h1>Sistema de Gestión de Residencia Universitaria</h1>
                        <p>UNMSM - Oficina General de Bienestar Universitario</p>
                    </div>
                </div>
                <div class="auth-buttons">
                    <button class="btn btn-outline" id="loginBtn">Iniciar Sesión</button>
                    <button class="btn btn-primary" id="registerBtn">Registrarse</button>
                </div>
            </div>
        </header>

        <!-- Navigation -->
        <nav>
            <div class="nav-container">
                <ul class="nav-menu">
                    <li><a href="#inicio">Inicio</a></li>
                    <li><a href="#convocatorias">Convocatorias</a></li>
                    <li><a href="#proceso">Proceso</a></li>
                    <li><a href="#requisitos">Requisitos</a></li>
                    <li><a href="#resultados">Resultados</a></li>
                    <li><a href="#contacto">Contacto</a></li>
                </ul>
            </div>
        </nav>

        <!-- Hero Section -->
        <section class="hero" id="inicio">
            <div class="hero-content">
                <h2>Beca de Vivienda Universitaria UNMSM</h2>
                <p>Gestiona tu postulación a la residencia universitaria de manera digital, transparente y eficiente</p>
                <div class="hero-buttons">
                    <button class="btn btn-primary" id="applyBtn">Postular Ahora</button>
                    <button class="btn btn-outline" id="infoBtn">Más Información</button>
                </div>
            </div>
        </section>

        <!-- Main Content -->
        <main class="container">
            <!-- Features Section -->
            <section>
                <h2 class="section-title">Funcionalidades del Sistema</h2>
                <div class="features">
                    <div class="feature-card">
                        <div class="feature-icon">📝</div>
                        <h3>Postulación Digital</h3>
                        <p>Registra tu postulación en línea con todos los documentos requeridos de forma segura y eficiente.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📊</div>
                        <h3>Seguimiento de Expediente</h3>
                        <p>Consulta el estado de tu postulación en tiempo real y recibe notificaciones sobre cada etapa del proceso.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🔍</div>
                        <h3>Evaluación Transparente</h3>
                        <p>Sistema de evaluación basado en criterios verificables que garantiza equidad en la asignación de plazas.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📋</div>
                        <h3>Gestión de Entrevistas</h3>
                        <p>Agenda y gestiona tus entrevistas socioeconómicas de manera sencilla a través del sistema.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🏠</div>
                        <h3>Asignación de Habitaciones</h3>
                        <p>Control y asignación transparente de las plazas disponibles en la residencia universitaria.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📈</div>
                        <h3>Reportes e Indicadores</h3>
                        <p>Generación de reportes para la toma de decisiones basada en datos reales del proceso.</p>
                    </div>
                </div>
            </section>

            <!-- Process Section -->
            <section id="proceso">
                <h2 class="section-title">Proceso de Postulación</h2>
                <div class="process-steps">
                    <div class="step">
                        <div class="step-number">1</div>
                        <h3>Registro</h3>
                        <p>Completa el formulario de postulación y adjunta los documentos requeridos.</p>
                    </div>
                    <div class="step">
                        <div class="step-number">2</div>
                        <h3>Evaluación Documental</h3>
                        <p>Revisión de documentos por parte del personal de la OGBU.</p>
                    </div>
                    <div class="step">
                        <div class="step-number">3</div>
                        <h3>Entrevista</h3>
                        <p>Entrevista socioeconómica con trabajadora social.</p>
                    </div>
                    <div class="step">
                        <div class="step-number">4</div>
                        <h3>Visita Domiciliaria</h3>
                        <p>Evaluación de condiciones mediante visita domiciliaria.</p>
                    </div>
                    <div class="step">
                        <div class="step-number">5</div>
                        <h3>Adjudicación</h3>
                        <p>Publicación de resultados y asignación de plazas.</p>
                    </div>
                </div>
            </section>

            <!-- Stats Section -->
            <section>
                <h2 class="section-title">Nuestro Impacto</h2>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">500+</div>
                        <p>Estudiantes Beneficiados</p>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">60%</div>
                        <p>Reducción en Tiempos de Procesamiento</p>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">95%</div>
                        <p>Satisfacción de Usuarios</p>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">100%</div>
                        <p>Trazabilidad en el Proceso</p>
                    </div>
                </div>
            </section>

            <!-- News Section -->
            <section>
                <h2 class="section-title">Noticias y Convocatorias</h2>
                <div class="news-grid">
                    <div class="news-card">
                        <div class="news-image" style="background-image: url('UNMSM.jpg');"></div>
                        <div class="news-content">
                            <div class="news-date">15 de Octubre, 2025</div>
                            <h3>Nueva Convocatoria Beca de Vivienda 2025-2</h3>
                            <p>Abierta la convocatoria para el semestre 2025-2. Postula hasta el 30 de noviembre.</p>
                            <a href="/login" class="btn btn-primary" style="margin-top: 10px; display: inline-block;">Postular Ahora</a>
                        </div>
                    </div>
                    <div class="news-card">
                        <div class="news-image" style="background-image: url('resultados.jpg');"></div>
                        <div class="news-content">
                            <div class="news-date">5 de Octubre, 2025</div>
                            <h3>Resultados Convocatoria 2025-1 Publicados</h3>
                            <p>Consulta los resultados de la convocatoria anterior en el portal oficial.</p>
                            <a href="/login" class="btn btn-primary" style="margin-top: 10px; display: inline-block;">Ver Resultados</a>
                        </div>
                    </div>
                    <div class="news-card">
                        <div class="news-image" style="background-image: url('capacitacion.jpeg');"></div>
                        <div class="news-content">
                            <div class="news-date">20 de Septiembre, 2025</div>
                            <h3>Capacitación Uso del Sistema SGRU</h3>
                            <p>Sesiones informativas sobre el uso del nuevo sistema de gestión de residencias.</p>
                            <a href="/login" class="btn btn-primary" style="margin-top: 10px; display: inline-block;">Más Información</a>
                        </div>
                    </div>
                </div>
            </section>
        </main>

        <!-- Footer -->
        <footer id="contacto">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Contacto</h3>
                    <ul class="contact-info">
                        <li><i>📍</i> Oficina General de Bienestar Universitario, Ciudad Universitaria, Lima 1</li>
                        <li><i>📞</i> Central Telefónica: 619 7000 - Anexo 7906</li>
                        <li><i>✉️</i> ogbu@unmsm.edu.pe</li>
                        <li><i>🕒</i> Horario: L-V 8:00 a.m. - 4:00 p.m.</li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Enlaces Rápidos</h3>
                    <ul class="footer-links">
                        <li><a href="#inicio">Inicio</a></li>
                        <li><a href="#convocatorias">Convocatorias</a></li>
                        <li><a href="#proceso">Proceso de Postulación</a></li>
                        <li><a href="#requisitos">Requisitos</a></li>
                        <li><a href="#resultados">Resultados</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Documentos</h3>
                    <ul class="footer-links">
                        <li><a href="#">Reglamento de Residencias</a></li>
                        <li><a href="#">Formatos de Postulación</a></li>
                        <li><a href="#">Guía de Usuario SGRU</a></li>
                        <li><a href="#">Preguntas Frecuentes</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                <p>&copy; 2025 Universidad Nacional Mayor de San Marcos - Oficina General de Bienestar Universitario. Todos los derechos reservados.</p>
            </div>
        </footer>

        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Login button - REDIRIGE AL LOGIN
                document.getElementById('loginBtn').addEventListener('click', function() {
                    window.location.href = '/login';
                });
                
                // Register button - REDIRIGE AL LOGIN (no hay registro separado)
                document.getElementById('registerBtn').addEventListener('click', function() {
                    window.location.href = '/login';
                });
                
                // Apply button - REDIRIGE AL LOGIN
                document.getElementById('applyBtn').addEventListener('click', function() {
                    window.location.href = '/login';
                });
                
                // Info button - HACE SCROLL a la sección de proceso
                document.getElementById('infoBtn').addEventListener('click', function() {
                    document.getElementById('proceso').scrollIntoView({ 
                        behavior: 'smooth',
                        block: 'start'
                    });
                });
                
                // Smooth scrolling para navegación
                document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                    anchor.addEventListener('click', function (e) {
                        e.preventDefault();
                        
                        const targetId = this.getAttribute('href');
                        if(targetId === '#') return;
                        
                        const targetElement = document.querySelector(targetId);
                        if(targetElement) {
                            window.scrollTo({
                                top: targetElement.offsetTop - 100,
                                behavior: 'smooth'
                            });
                        }
                    });
                });
            });
        </script>
    </body>
    </html>
    '''

# Página de login (manteniendo el diseño original del app.py)
@app.route('/login')
def login_page():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Iniciar Sesión - SGRU UNMSM</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
                --primary-color: #003366;
                --secondary-color: #990000;
                --accent-color: #0066cc;
                --light-color: #f5f5f5;
                --dark-color: #333333;
                --card-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s ease;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            body {
                background: url('UNMSM.jpg') center/cover no-repeat fixed;
                color: var(--dark-color);
                line-height: 1.6;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                position: relative;
            }
            
            body::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 51, 102, 0.85);
                z-index: 1;
            }
            
            .login-container {
                width: 100%;
                max-width: 1000px;
                display: flex;
                background: white;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: var(--card-shadow);
                animation: fadeIn 0.8s ease;
                position: relative;
                z-index: 2;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .login-left {
                flex: 1;
                background: linear-gradient(135deg, var(--primary-color), #004080);
                color: white;
                padding: 3rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            
            .login-left::before {
                content: '';
                position: absolute;
                top: -50px;
                right: -50px;
                width: 200px;
                height: 200px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
            }
            
            .login-left::after {
                content: '';
                position: absolute;
                bottom: -80px;
                left: -80px;
                width: 250px;
                height: 250px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
            }
            
            .logo-section {
                display: flex;
                align-items: center;
                margin-bottom: 2rem;
            }
            
            .logo {
                width: 120px;
                height: 120px;
                background: white;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 20px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }
            
            .logo-text h1 {
                font-size: 1.8rem;
                margin-bottom: 8px;
                text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
                line-height: 1.2;
            }
            
            .logo-text p {
                opacity: 0.9;
                font-size: 1rem;
            }
            
            .welcome-text {
                margin-bottom: 2.5rem;
            }
            
            .welcome-text h2 {
                font-size: 2.5rem;
                margin-bottom: 1rem;
                line-height: 1.2;
                font-weight: 700;
            }
            
            .welcome-text p {
                font-size: 1.2rem;
                opacity: 0.9;
                line-height: 1.6;
            }
            
            .features-list {
                list-style: none;
                margin-top: 2rem;
            }
            
            .features-list li {
                margin-bottom: 1.2rem;
                display: flex;
                align-items: center;
                font-size: 1.1rem;
            }
            
            .features-list i {
                margin-right: 15px;
                background: rgba(255, 255, 255, 0.2);
                width: 35px;
                height: 35px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
            }
            
            .login-right {
                flex: 1;
                padding: 3rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
                background: white;
            }
            
            .login-header {
                text-align: center;
                margin-bottom: 2.5rem;
            }
            
            .login-header h2 {
                font-size: 2.2rem;
                color: var(--primary-color);
                margin-bottom: 0.8rem;
                font-weight: 700;
            }
            
            .login-header p {
                color: #666;
                font-size: 1.2rem;
                font-weight: 500;
            }
            
            .form-group {
                margin-bottom: 1.8rem;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 0.8rem;
                font-weight: 600;
                color: var(--dark-color);
                font-size: 1.1rem;
            }
            
            .input-with-icon {
                position: relative;
            }
            
            .input-with-icon i {
                position: absolute;
                left: 18px;
                top: 50%;
                transform: translateY(-50%);
                color: #999;
                font-size: 1.2rem;
            }
            
            .form-control {
                width: 100%;
                padding: 16px 20px 16px 55px;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                font-size: 1.1rem;
                transition: var(--transition);
                background: #fafafa;
            }
            
            .form-control:focus {
                border-color: var(--accent-color);
                outline: none;
                box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.2);
                background: white;
            }
            
            .form-actions {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 2rem;
            }
            
            .btn {
                padding: 16px 30px;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                font-weight: 600;
                transition: var(--transition);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                font-size: 1.1rem;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, var(--accent-color), #0044cc);
                color: white;
                flex: 1;
                font-weight: 700;
            }
            
            .btn-primary:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(0, 102, 204, 0.4);
            }
            
            .forgot-password {
                color: var(--accent-color);
                text-decoration: none;
                font-size: 1rem;
                transition: var(--transition);
                font-weight: 500;
            }
            
            .forgot-password:hover {
                text-decoration: underline;
            }
            
            .error-message {
                background: #ffebee;
                color: #d32f2f;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 1.5rem;
                text-align: center;
                border: 1px solid #ffcdd2;
                display: none;
                font-weight: 500;
            }
            
            .credentials-info {
                background: #e8f4ff;
                padding: 15px;
                border-radius: 10px;
                margin-top: 2rem;
                border-left: 4px solid var(--accent-color);
            }
            
            .credentials-info h4 {
                color: var(--primary-color);
                margin-bottom: 10px;
                font-size: 1.1rem;
            }
            
            .credentials-info p {
                font-size: 0.95rem;
                color: #555;
                line-height: 1.5;
            }
            
            .back-home {
                text-align: center;
                margin-top: 1.5rem;
            }
            
            .back-home a {
                color: var(--primary-color);
                text-decoration: none;
                font-weight: 500;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }
            
            .back-home a:hover {
                text-decoration: underline;
            }
            
            /* Responsive Design */
            @media (max-width: 900px) {
                .login-container {
                    flex-direction: column;
                    max-width: 500px;
                }
                
                .login-left {
                    padding: 2.5rem;
                }
                
                .login-right {
                    padding: 2.5rem;
                }
                
                .logo-section {
                    flex-direction: column;
                    text-align: center;
                }
                
                .logo {
                    margin-right: 0;
                    margin-bottom: 20px;
                }
            }
            
            @media (max-width: 500px) {
                .login-left, .login-right {
                    padding: 2rem;
                }
                
                .welcome-text h2 {
                    font-size: 2rem;
                }
                
                .login-header h2 {
                    font-size: 1.8rem;
                }
                
                .btn {
                    padding: 14px 25px;
                }
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-left">
                <div class="logo-section">
                    <div class="logo">
                        <img src="unmsm2.png" alt="UNMSM" style="width: 100%; height: 100%; object-fit: contain; border-radius: 8px;">
                    </div>
                    <div class="logo-text">
                        <h1>Sistema de Gestión de Residencia Universitaria</h1>
                        <p>UNMSM - Oficina General de Bienestar Universitario</p>
                    </div>
                </div>
                
                <div class="welcome-text">
                    <h2>Bienvenido al SGRU</h2>
                    <p>Accede al sistema integral de gestión de residencias universitarias</p>
                </div>
                
                <ul class="features-list">
                    <li><i class="fas fa-shield-alt"></i> Autenticación segura institucional</li>
                    <li><i class="fas fa-bolt"></i> Procesos digitalizados y optimizados</li>
                    <li><i class="fas fa-chart-line"></i> Seguimiento en tiempo real</li>
                    <li><i class="fas fa-users"></i> Gestión integral de usuarios</li>
                </ul>
            </div>
            
            <div class="login-right">
                <div class="login-header">
                    <h2>Iniciar Sesión</h2>
                    <p>Ingresa tus credenciales para acceder al sistema</p>
                </div>
                
                <div class="error-message" id="error-message">
                    <i class="fas fa-exclamation-circle"></i> Usuario o contraseña incorrectos
                </div>
                
                <form method="POST" action="/procesar-login" id="login-form">
                    <div class="form-group">
                        <label for="username">Usuario o Código</label>
                        <div class="input-with-icon">
                            <i class="fas fa-user"></i>
                            <input type="text" id="username" name="codigo" class="form-control" placeholder="Ingresa tu código o usuario" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Contraseña</label>
                        <div class="input-with-icon">
                            <i class="fas fa-lock"></i>
                            <input type="password" id="password" name="password" class="form-control" placeholder="Ingresa tu contraseña" required>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary" id="submit-btn">
                            <i class="fas fa-sign-in-alt"></i> Ingresar al Sistema
                        </button>
                    </div>
                </form>
                
                <div class="credentials-info">
                    <h4><i class="fas fa-info-circle"></i> Credenciales de Prueba</h4>
                    <p>
                        <strong>Residente:</strong> 20210001 / sanmarcos123<br>
                        <strong>Administrativo:</strong> ADMIN001 / sanmarcos123<br>
                        <strong>Postulante:</strong> 20210002 / sanmarcos123<br>
                        <strong>Trabajador Social:</strong> TSOCIAL01 / sanmarcos123
                    </p>
                </div>
                
                <div class="back-home">
                    <a href="/">
                        <i class="fas fa-arrow-left"></i> Volver a la página principal
                    </a>
                </div>
            </div>
        </div>

        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const errorMessage = document.getElementById('error-message');
                const loginForm = document.getElementById('login-form');
                const submitBtn = document.getElementById('submit-btn');
                
                // Mostrar mensaje de error si viene del servidor
                ''' + ('''
                errorMessage.style.display = 'block';
                ''' if request.args.get('error') else '') + '''
                
                // Form submission loading state
                loginForm.addEventListener('submit', function(e) {
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verificando...';
                    submitBtn.disabled = true;
                    
                    // Permitir que el formulario se envíe normalmente
                    return true;
                });
                
                // Ocultar mensaje de error al empezar a escribir
                const inputs = document.querySelectorAll('input');
                inputs.forEach(input => {
                    input.addEventListener('input', function() {
                        errorMessage.style.display = 'none';
                    });
                });
            });
        </script>
    </body>
    </html>
    '''

# Procesar login
@app.route('/procesar-login', methods=['POST'])
def procesar_login():
    codigo = request.form['codigo']
    password = request.form['password']
    
    conn = sqlite3.connect('sgru.db')
    usuario = conn.execute(
        "SELECT codigo, rol, nombres FROM usuarios WHERE codigo = ? AND password = ?",
        (codigo, password)
    ).fetchone()
    conn.close()
    
    if usuario:
        session['usuario'] = {
            'codigo': usuario[0],
            'rol': usuario[1],
            'nombres': usuario[2]
        }
        
        # REDIRIGIR A LOS PORTALES
        if usuario[1] == 'RESIDENTE':
            return redirect('/residente')
        elif usuario[1] == 'ADMINISTRATIVO':
            return redirect('/personal')
        elif usuario[1] == 'POSTULANTE':
            return redirect('/postulante')
        elif usuario[1] == 'TRABAJADOR_SOCIAL':
            return redirect('/trabajador-social')
    else:
        return redirect('/login?error=1')

# Rutas para los portales
@app.route('/residente')
def residente():
    if 'usuario' not in session or session['usuario']['rol'] != 'RESIDENTE':
        return redirect('/login')
    return send_file('residente.html')

@app.route('/personal')
def personal():
    if 'usuario' not in session or session['usuario']['rol'] != 'ADMINISTRATIVO':
        return redirect('/login')
    return send_file('Personal.html')

@app.route('/postulante')
def postulante():
    if 'usuario' not in session or session['usuario']['rol'] != 'POSTULANTE':
        return redirect('/login')
    return send_file('postulante.html')

@app.route('/trabajador-social')
def trabajador_social():
    if 'usuario' not in session or session['usuario']['rol'] != 'TRABAJADOR_SOCIAL':
        return redirect('/login')
    return send_file('trabajador-social.html')

# Ruta para archivos estáticos
@app.route('/<filename>')
def serve_static_files(filename):
    excluded_routes = ['', 'login', 'procesar-login', 'residente', 'personal', 'postulante', 'trabajador-social', 'logout']
    
    if filename not in excluded_routes and os.path.isfile(filename):
        return send_file(filename)
    else:
        return "Archivo no encontrado", 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)