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

# Ruta de login con diseño UNMSM
@app.route('/')
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
                justify-content: space-between;
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
                
                <form method="POST" action="/login" id="login-form">
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
                        <a href="#" class="forgot-password">
                            <i class="fas fa-key"></i> ¿Olvidaste tu contraseña?
                        </a>
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
                        <strong>Postulante:</strong> 20210002 / sanmarcos123
                    </p>
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

# Procesar login y redirigir (MANTENIENDO LA FUNCIONALIDAD)
@app.route('/login', methods=['POST'])
def login():
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
        
        # REDIRIGIR A TUS ARCHIVOS HTML EXISTENTES
        if usuario[1] == 'RESIDENTE':
            return redirect('/residente')
        elif usuario[1] == 'ADMINISTRATIVO':
            return redirect('/personal')
        elif usuario[1] == 'POSTULANTE':
            return redirect('/postulante')
        elif usuario[1] == 'TRABAJADOR_SOCIAL':
            return redirect('/trabajador-social')
    else:
        return redirect('/?error=1')

# Rutas para servir tus archivos HTML (MANTENIENDO LA FUNCIONALIDAD)
@app.route('/residente')
def residente():
    if 'usuario' not in session or session['usuario']['rol'] != 'RESIDENTE':
        return redirect('/')
    return send_file('residente.html')

@app.route('/personal')
def personal():
    if 'usuario' not in session or session['usuario']['rol'] != 'ADMINISTRATIVO':
        return redirect('/')
    return send_file('Personal.html')

@app.route('/postulante')
def postulante():
    if 'usuario' not in session or session['usuario']['rol'] != 'POSTULANTE':
        return redirect('/')
    return send_file('postulante.html')

@app.route('/trabajador-social')
def trabajador_social():
    if 'usuario' not in session or session['usuario']['rol'] != 'TRABAJADOR_SOCIAL':
        return redirect('/')
    return send_file('trabajador-social.html')

# Ruta para archivos estáticos
@app.route('/<filename>')
def serve_static_files(filename):
    excluded_routes = ['', 'login', 'residente', 'personal', 'postulante', 'trabajador-social', 'logout']
    
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