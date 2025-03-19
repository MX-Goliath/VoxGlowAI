// Анимация пульсирующей сферы для веб-интерфейса VoxGlowAI
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('sphereCanvas');
    const ctx = canvas.getContext('2d');
    
    // Размер canvas в соответствии с размером окна
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Настройки сферы
    const sphereSettings = {
        radius: Math.min(canvas.width, canvas.height) * 0.25, // Радиус основной сферы
        centerX: canvas.width / 2,
        centerY: canvas.height / 2,
        speed: 0.002,
        pulseSpeed: 0.005,
        noiseIntensity: 0.1, // Уменьшаем искажение сферы
        resolution: 60, // Разрешение сферы (количество сегментов)
        particles: 120, // Количество частиц вокруг сферы
        colorIntensity: 1, // Интенсивность цвета
        colorHue: 0, // Оттенок (0-1)
        state: 'idle' // Текущее состояние анимации
    };
    
    // Настройки цветов из CSS переменных
    const getColor = (varName) => {
        return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
    };
    
    const colors = {
        sphereColor1: getColor('--sphere-color-1'),
        sphereColor2: getColor('--sphere-color-2'),
        sphereColor3: getColor('--sphere-color-3'),
        particleColor1: getColor('--particle-color-1'),
        particleColor2: getColor('--particle-color-2')
    };
    
    // Создаем массив частиц
    let sphereParticles = [];
    
    // Инициализация частиц
    function initParticles() {
        sphereParticles = [];
        
        // Обновляем положение центра сферы
        sphereSettings.centerX = canvas.width / 2;
        sphereSettings.centerY = canvas.height / 2;
        sphereSettings.radius = Math.min(canvas.width, canvas.height) * 0.25;
        
        // Создаем частицы вокруг сферы
        for (let i = 0; i < sphereSettings.particles; i++) {
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.random() * Math.PI;
            const radiusOffset = (Math.random() * 0.5 + 0.8) * sphereSettings.radius;
            
            sphereParticles.push({
                theta: theta,
                phi: phi,
                radius: radiusOffset,
                size: Math.random() * 3 + 1,
                opacity: Math.random() * 0.8 + 0.2,
                velocity: (Math.random() * 2 - 1) * 0.002,
                velocityPhi: (Math.random() * 2 - 1) * 0.001,
                color: Math.random() > 0.5 ? colors.particleColor1 : colors.particleColor2
            });
        }
    }
    
    // Инициализируем частицы
    initParticles();
    window.addEventListener('resize', initParticles);
    
    // Функция для преобразования сферических координат в декартовы
    function sphericalToCartesian(radius, theta, phi) {
        return {
            x: radius * Math.sin(phi) * Math.cos(theta),
            y: radius * Math.sin(phi) * Math.sin(theta),
            z: radius * Math.cos(phi)
        };
    }
    
    // Переменные для анимации
    let time = 0;
    let pulsePhase = 0;
    
    // Обработчик событий анимации
    canvas.addEventListener('animationUpdate', (event) => {
        const type = event.detail.type;
        
        switch (type) {
            case 'typing':
                // Увеличиваем скорость пульсации и добавляем небольшое движение
                sphereSettings.pulseSpeed = 0.008;
                sphereSettings.noiseIntensity = 0.15;
                sphereSettings.speed = 0.003;
                sphereSettings.state = 'typing';
                break;
                
            case 'message-sent':
                // Быстрая пульсация при отправке сообщения
                sphereSettings.pulseSpeed = 0.02;
                sphereSettings.noiseIntensity = 0.18;
                sphereSettings.state = 'message-sent';
                
                // Через 1 секунду возвращаемся к состоянию ожидания
                setTimeout(() => {
                    sphereSettings.pulseSpeed = 0.01;
                    sphereSettings.noiseIntensity = 0.15;
                    sphereSettings.state = 'waiting';
                }, 1000);
                break;
                
            case 'message-received':
                // Яркая пульсация при получении сообщения
                sphereSettings.pulseSpeed = 0.015;
                sphereSettings.noiseIntensity = 0.17;
                sphereSettings.colorIntensity = 1.2;
                sphereSettings.state = 'message-received';
                
                // Плавно возвращаемся к состоянию покоя
                setTimeout(() => {
                    sphereSettings.pulseSpeed = 0.008;
                    sphereSettings.noiseIntensity = 0.1;
                    sphereSettings.colorIntensity = 1;
                    sphereSettings.state = 'idle';
                }, 1500);
                break;
                
            case 'error':
                // Быстрая и резкая пульсация при ошибке
                sphereSettings.pulseSpeed = 0.03;
                sphereSettings.noiseIntensity = 0.2;
                sphereSettings.colorHue = 0.9; // Красноватый оттенок
                sphereSettings.state = 'error';
                
                // Через 2 секунды возвращаемся к нормальному состоянию
                setTimeout(() => {
                    sphereSettings.pulseSpeed = 0.005;
                    sphereSettings.noiseIntensity = 0.1;
                    sphereSettings.colorHue = 0;
                    sphereSettings.state = 'idle';
                }, 2000);
                break;
                
            case 'reset':
                // Сброс всех настроек анимации
                sphereSettings.pulseSpeed = 0.005;
                sphereSettings.noiseIntensity = 0.1;
                sphereSettings.speed = 0.002;
                sphereSettings.colorIntensity = 1;
                sphereSettings.colorHue = 0;
                sphereSettings.state = 'idle';
                break;
                
            case 'idle':
            default:
                // Спокойное состояние
                sphereSettings.pulseSpeed = 0.005;
                sphereSettings.noiseIntensity = 0.1;
                sphereSettings.speed = 0.002;
                sphereSettings.state = 'idle';
                break;
        }
    });
    
    // Функция анимации
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Обновляем время
        time += sphereSettings.speed;
        pulsePhase += sphereSettings.pulseSpeed;
        
        // Пульсация радиуса
        const pulseRadius = sphereSettings.radius * (1 + Math.sin(pulsePhase) * 0.05);
        
        // Отрисовка частиц за сферой (с меньшей непрозрачностью)
        sphereParticles.forEach(particle => {
            // Обновляем положение частицы
            particle.theta += particle.velocity;
            particle.phi += particle.velocityPhi;
            
            // Преобразуем в декартовы координаты
            const position = sphericalToCartesian(particle.radius, particle.theta, particle.phi);
            
            // Если частица за сферой, рисуем с меньшей непрозрачностью
            if (position.z < 0) {
                const x = position.x + sphereSettings.centerX;
                const y = position.y + sphereSettings.centerY;
                
                ctx.fillStyle = particle.color;
                ctx.globalAlpha = particle.opacity * 0.3;
                ctx.beginPath();
                ctx.arc(x, y, particle.size, 0, Math.PI * 2);
                ctx.fill();
            }
        });
        
        // Цвета с учетом состояния
        let sphereColor1 = colors.sphereColor1;
        let sphereColor2 = colors.sphereColor2;
        let sphereColor3 = colors.sphereColor3;
        
        // Изменение цвета для разных состояний
        if (sphereSettings.state === 'error') {
            sphereColor1 = '#ff5555';
            sphereColor3 = '#ff3077';
        } else if (sphereSettings.colorHue !== 0) {
            // Применяем оттенок, если он не нулевой
            // Здесь можно реализовать изменение цвета, но для простоты оставим как есть
        }
        
        // Создаем градиент для сферы
        const gradient = ctx.createRadialGradient(
            sphereSettings.centerX, sphereSettings.centerY, 0,
            sphereSettings.centerX, sphereSettings.centerY, pulseRadius
        );
        
        gradient.addColorStop(0, sphereColor1);
        gradient.addColorStop(0.5, sphereColor2);
        gradient.addColorStop(1, sphereColor3);
        
        // Отрисовка основной сферы
        ctx.globalAlpha = 0.2;
        ctx.beginPath();
        ctx.arc(sphereSettings.centerX, sphereSettings.centerY, pulseRadius, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.fill();
        
        // Рисуем сетку на сфере
        drawSphereGrid(pulseRadius, sphereSettings.resolution, sphereSettings.noiseIntensity);
        
        // Отрисовка частиц перед сферой
        ctx.globalAlpha = 1;
        sphereParticles.forEach(particle => {
            // Преобразуем в декартовы координаты
            const position = sphericalToCartesian(particle.radius, particle.theta, particle.phi);
            
            // Если частица перед сферой, рисуем с полной непрозрачностью
            if (position.z >= 0) {
                const x = position.x + sphereSettings.centerX;
                const y = position.y + sphereSettings.centerY;
                
                ctx.fillStyle = particle.color;
                ctx.globalAlpha = particle.opacity;
                ctx.beginPath();
                ctx.arc(x, y, particle.size, 0, Math.PI * 2);
                ctx.fill();
            }
        });
        
        // Сброс значения globalAlpha
        ctx.globalAlpha = 1;
        
        // Световые эффекты в зависимости от состояния
        let glowColor = 'rgba(211, 113, 255, 0.03)';
        let glowRadius = pulseRadius * 1.2;
        
        if (sphereSettings.state === 'typing') {
            glowColor = 'rgba(211, 113, 255, 0.05)';
            glowRadius = pulseRadius * 1.25;
        } else if (sphereSettings.state === 'message-sent') {
            glowColor = 'rgba(211, 113, 255, 0.08)';
            glowRadius = pulseRadius * 1.3;
        } else if (sphereSettings.state === 'message-received') {
            glowColor = 'rgba(211, 113, 255, 0.1)';
            glowRadius = pulseRadius * 1.35;
        } else if (sphereSettings.state === 'error') {
            glowColor = 'rgba(255, 85, 85, 0.08)';
            glowRadius = pulseRadius * 1.3;
        }
        
        // Рисуем свечение
        ctx.fillStyle = glowColor;
        ctx.beginPath();
        ctx.arc(sphereSettings.centerX, sphereSettings.centerY, glowRadius, 0, Math.PI * 2);
        ctx.fill();
        
        requestAnimationFrame(animate);
    }
    
    // Функция для рисования сетки на сфере
    function drawSphereGrid(radius, resolution, noiseIntensity) {
        const segments = resolution;
        const noiseScale = 0.1;
        
        // Горизонтальные окружности
        for (let i = 1; i < segments / 2; i++) {
            const phi = (i / (segments / 2)) * Math.PI;
            const segmentRadius = radius * Math.sin(phi);
            const y = sphereSettings.centerY + radius * Math.cos(phi);
            
            ctx.globalAlpha = 0.1;
            ctx.strokeStyle = '#d371ff';
            ctx.lineWidth = 1;
            ctx.beginPath();
            
            // Рисуем окружность с небольшим шумом
            for (let j = 0; j <= segments; j++) {
                const theta = (j / segments) * Math.PI * 2;
                
                // Добавляем небольшой шум к радиусу, зависящий от времени
                const noise = Math.sin(time + theta * 3) * Math.cos(phi * 4 + time) * noiseIntensity;
                const adjustedRadius = segmentRadius * (1 + noise * noiseScale);
                
                const x = sphereSettings.centerX + Math.cos(theta) * adjustedRadius;
                
                if (j === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            
            ctx.closePath();
            ctx.stroke();
        }
        
        // Вертикальные дуги
        for (let i = 0; i < segments; i++) {
            const theta = (i / segments) * Math.PI * 2;
            
            ctx.globalAlpha = 0.1;
            ctx.strokeStyle = '#d371ff';
            ctx.lineWidth = 1;
            ctx.beginPath();
            
            // Рисуем дугу с небольшим шумом
            for (let j = 0; j <= segments; j++) {
                const phi = (j / segments) * Math.PI;
                
                // Добавляем небольшой шум к радиусу, зависящий от времени
                const noise = Math.sin(time + theta * 3) * Math.cos(phi * 4 + time) * noiseIntensity;
                const adjustedRadius = radius * (1 + noise * noiseScale);
                
                const x = sphereSettings.centerX + Math.sin(phi) * Math.cos(theta) * adjustedRadius;
                const y = sphereSettings.centerY + Math.cos(phi) * adjustedRadius;
                
                if (j === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            
            ctx.stroke();
        }
    }
    
    // Запускаем анимацию
    animate();
    
    // Обработка отправки сообщения для изменения анимации
    document.getElementById('chatForm').addEventListener('submit', () => {
        sphereSettings.pulseSpeed = 0.02;
        setTimeout(() => {
            sphereSettings.pulseSpeed = 0.005;
        }, 1000);
    });
}); 