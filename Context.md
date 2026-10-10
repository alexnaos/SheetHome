Вот полная, финальная и технически точная схема. Здесь исправлена ошибка с «висящими» контактами реле, которые вызывали у вас вопросы. Теперь на схеме четко видно, как сквозь реле замыкается сигнальная петля запуска генератора.
Скопируйте этот обновленный код в ваш HTML-файл. В нем полностью прорисованы все 5 жил кабеля управления, 4 силовых провода и связи между АВР и промежуточным реле.

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Полная монтажная схема АВР TOMZN + Реле + ATS 5-Pin</title>
    <style>
        :root {
            --bg-color: #0b0c10;
            --card-bg: #141722;
            --border-color: #242936;
            --text-main: #f8f9fa;
            --text-muted: #959da5;
            
            /* Цвета проводов */
            --color-l-city: #ea4335;   /* Фаза Город */
            --color-l-gen: #ff9900;    /* Фаза Генератор */
            --color-n: #4285f4;        /* Ноль */
            --color-pe: #34a853;       /* Земля */
            --color-ctrl: #fbbc05;     /* Питание контроля 220В */
            --color-dry: #a142f4;      /* Сухой контакт старта */
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 1300px;
            margin: 0 auto;
        }

        header {
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 25px;
        }

        h1 { font-size: 22px; margin: 0 0 5px 0; }
        .desc { font-size: 14px; color: var(--text-muted); margin: 0; }

        .layout {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 20px;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 20px;
        }

        .workspace {
            background-color: #050608;
            border-radius: 8px;
            padding: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .controls {
            display: flex;
            gap: 10px;
            width: 100%;
            margin-bottom: 20px;
        }

        button {
            background-color: #212529;
            border: 1px solid #3a3f44;
            color: #fff;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.15s ease;
        }

        button.active-city { background-color: #1a73e8; border-color: #1a73e8; color: white; }
        button.active-gen { background-color: #e67e22; border-color: #e67e22; color: white; }

        .sidebar { display: flex; flex-direction: column; gap: 20px; }
        .section-title { font-size: 13px; font-weight: bold; text-transform: uppercase; color: var(--text-muted); margin-bottom: 12px; letter-spacing: 0.5px; }
        
        .wire-ref { display: flex; align-items: center; margin-bottom: 10px; font-size: 13px; }
        .wire-color { width: 20px; height: 16px; border-radius: 3px; margin-right: 12px; flex-shrink: 0; }

        .m-table { width: 100%; border-collapse: collapse; font-size: 12px; }
        .m-table th, .m-table td { padding: 8px; text-align: left; border-bottom: 1px solid var(--border-color); }
        .m-table th { color: var(--text-muted); font-weight: 500; }

        .live-wire { stroke-dasharray: 5; animation: none; }
        .running { animation: pulse 5s linear infinite; }
        @keyframes pulse { to { stroke-dashoffset: -50; } }
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>Нормальная схема расключения автоматики АВР</h1>
        <p class="desc">Полное соединение всех контактов: Сеть, Блок TOMZN, Промежуточное реле, Защитный автомат 2А и Контрольный разъем генератора GX16</p>
    </header>

    <div class="layout">
        <!-- Левая часть: Интерактивный интерактивный щит -->
        <div class="card">
            <div class="workspace">
                <div class="controls">
                    <button id="btnStateCity" class="active-city" onclick="changeState('city')">Режим: Городская сеть (Норма)</button>
                    <button id="btnStateGen" onclick="changeState('gen')">Режим: Работа от генератора (Авария)</button>
                </div>

                <svg width="880" height="600" viewBox="0 0 880 600" fill="none" xmlns="http://w3.org">
                    <rect width="880" height="600" fill="#08090c" rx="8"/>

                    <!-- МОДУЛЬ: Сеть здания -->
                    <rect x="30" y="40" width="130" height="80" rx="6" fill="#181a20" stroke="#2a2f3b" stroke-width="2"/>
                    <text x="95" y="75" fill="#fff" font-size="13" font-weight="bold" text-anchor="middle">Ввод Сети 220В</text>
                    <text x="95" y="95" fill="#1a73e8" font-size="11" text-anchor="middle">Городской свет</text>

                    <!-- МОДУЛЬ: Двухполюсный автомат 2А -->
                    <rect x="230" y="40" width="80" height="80" rx="6" fill="#181a20" stroke="#fbbc05" stroke-width="1.5"/>
                    <text x="270" y="75" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Автомат</text>
                    <text x="270" y="95" fill="#fbbc05" font-size="12" font-weight="bold" text-anchor="middle">2А (2P)</text>

                    <!-- МОДУЛЬ: Промежуточное реле развязки логики -->
                    <rect x="560" y="40" width="150" height="120" rx="6" fill="#181a20" stroke="#a142f4" stroke-width="1.5"/>
                    <text x="635" y="70" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">Пром. Реле</text>
                    <text x="635" y="90" fill="#888" font-size="10" text-anchor="middle">(Катушка 220В)</text>
                    
                    <!-- Клеммные контакты реле -->
                    <circle cx="590" cy="130" r="10" fill="#242936"/><text x="590" y="133" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">11</text>
                    <circle cx="635" cy="130" r="10" fill="#242936"/><text x="635" y="133" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">12</text>
                    <circle cx="680" cy="130" r="10" fill="#242936"/><text x="680" y="133" fill="#fff" font-size="9" font-weight="bold" text-anchor="middle">A1</text>
                    <circle cx="680" cy="25" r="10" fill="#242936"/><text x="680" y="28" fill="#fff" font-size="9" font-weight="bold" text-anchor="middle">A2</text>

                    <!-- МОДУЛЬ: Блок АВР TOMZN -->
                    <rect x="360" y="200" width="220" height="210" rx="8" fill="#1c1f26" stroke="#3a4050" stroke-width="2"/>
                    <text x="470" y="230" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">TOMZN TOQ5-63/2P</text>
                    
                    <!-- Силовые зажимы АВР -->
                    <rect x="385" y="260" width="50" height="35" rx="4" fill="#0d0e12"/><text x="410" y="282" fill="#1a73e8" font-size="11" font-weight="bold" text-anchor="middle">Вход А</text>
                    <rect x="495" y="260" width="50" height="35" rx="4" fill="#0d0e12"/><text x="520" y="282" fill="#e67e22" font-size="11" font-weight="bold" text-anchor="middle">Вход B</text>
                    
                    <!-- Управляющая колодка выходов АВР -->
                    <rect x="385" y="350" width="40" height="30" rx="3" fill="#242936"/><text x="405" y="369" fill="#fff" font-size="11" text-anchor="middle">AR</text>
                    <rect x="435" y="350" width="40" height="30" rx="3" fill="#242936"/><text x="455" y="369" fill="#fff" font-size="11" text-anchor="middle">AN</text>

                    <!-- МОДУЛЬ: Инверторный Генератор -->
                    <rect x="30" y="440" width="180" height="130" rx="6" fill="#181a20" stroke="#e67e22" stroke-width="2"/>
                    <text x="120" y="475" fill="#fff" font-size="13" font-weight="bold" text-anchor="middle">Инверторный генератор</text>
                    
                    <!-- Круглый Разъем на Панели Генератора GX16 -->
                    <circle cx="170" cy="520" r="22" fill="#090a0d" stroke="#a142f4" stroke-width="2"/>
                    <text x="170" y="524" fill="#a142f4" font-size="11" font-weight="bold" text-anchor="middle">GX16</text>

                    <!-- МОДУЛЬ: Нагрузка (Электрощит Жилого Дома) -->
                    <rect x="680" y="250" width="160" height="90" rx="6" fill="#181a20" stroke="#34a853" stroke-width="2"/>
                    <text x="760" y="300" fill="#fff" font-size="13" font-weight="bold" text-anchor="middle">Домашний Щит</text>

                    <!-- Главная заземляющая шина PE щита -->
                    <rect x="360" y="550" width="480" height="20" rx="4" fill="#1e4620"/>
                    <text x="600" y="564" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">ГЛАВНАЯ ШИНА ЗАЗЕМЛЕНИЯ (PE)</text>


                    <!-- ================= СИЛОВЫЕ ТРАССЫ И КОММУТАЦИЯ ================= -->

                    <!-- Город -> АВР (Вход А) -->
                    <path id="powerCityL" class="live-wire running" d="M 160 70 L 410 70 L 410 260" stroke="#ea4335" stroke-width="3.5"/>
                    <path id="powerCityN" class="live-wire running" d="M 160 85 L 395 85 L 395 260" stroke="#4285f4" stroke-width="3.5"/>

                    <!-- Запитка вспомогательного автомата 2А от Входа А Города -->
                    <path d="M 230 70 L 160 70" stroke="#ea4335" stroke-width="1.5" stroke-dasharray="3"/>
                    <path d="M 230 85 L 160 85" stroke="#4285f4" stroke-width="1.5" stroke-dasharray="3"/>

                    <!-- Выход автомата 2А -> Разъем генератора GX16 (Пины 1 и 2) -->
                    <path id="sigPin1" class="live-wire running" d="M 250 120 L 250 415 L 155 415 L 155 500" stroke="#fbbc05" stroke-width="2"/>


Цветовая кодировка проводников


Силовая Фаза Города (L) — ВВГнг-LS 3x6



Силовая Фаза Генератора — ВВГнг-LS 3x4



Рабочий Ноль (N)



Линия контроля 220В (через автомат 2А)



«Сухой контакт» старта (Пины 3 и 4)



Защитная земля (PE) — ПуГВ 6 мм²
Полная Монтажная Карта Жила-в-Контакт
function changeState(state) {
const bCity = document.getElementById('btnStateCity');
const bGen = document.getElementById('btnStateGen');
// Линии токов
const pCityL = document.getElementById('powerCityL');
const pCityN = document.getElementById('powerCityN');
const sP1 = document.getElementById('sigPin1');
const sP2 = document.getElementById('sigPin2');
const rLA1 = document.getElementById('relayLineA1');
const rLA2 = document.getElementById('relayLineA2');
const lLL = document.getElementById('loadLineL');
const lLN = document.getElementById('loadLineN');
const pGenL = document.getElementById('powerGenL');
const pGenN = document.getElementById('powerGenN');
const sP3 = document.getElementById('sigPin3');
const sP4 = document.getElementById('sigPin4');
if (state === 'city') {
bCity.className = 'active-city'; bGen.className = '';
pCityL.classList.add('running'); pCityN.classList.add('running');
sP1.classList.add('running'); sP2.classList.add('running');
rLA1.classList.add('running'); rLA2.classList.add('running');
lLL.classList.add('running'); lLN.classList.add('running');
pGenL.classList.remove('running'); pGenN.classList.remove('running');
sP3.classList.remove('running'); sP4.classList.remove('running');
} else {
bCity.className = ''; bGen.className = 'active-gen';
pCityL.classList.remove('running'); pCityN.classList.remove('running');
sP1.classList.remove('running'); sP2.classList.remove('running');
rLA1.classList.remove('running'); rLA2.classList.remove('running');
lLL.classList.remove('running'); lLN.classList.remove('running');
pGenL.classList.add('running'); pGenN.classList.add('running');
sP3.classList.add('running'); sP4.classList.add('running');
}
}


### 🧱 Итоговая спецификация комплектующих электрощита

| Элемент схемы | Оптимальные параметры и номинал | Назначение в щите |
| :--- | :--- | :--- |
| **Блок АВР (TOMZN)** | TOQ5-63/2P (Двухполюсный, Однофазный, **63 А**) | Основная силовая коммутация нагрузок дома. |
| **Автомат управления** | 2P (Двухполюсный), Номинал **2 Ампера** | Защита встроенной платы генератора по линии контроля 220В. |
| **Промежуточное реле** | Модульное на DIN-рейку, Катушка питания **220В** (Контакты 11, 12, A1, A2) | Изоляция сигнальных цепей и безопасная подача «сухого контакта». |
| **Разъем управления** | Промышленный круглый штекер авиационного типа **GX16-5 Pin** | Надежное соединение контрольного кабеля с панелью инвертора. |

<FollowUp>
Теперь, когда схема полностью готова к сборке, подскажите: вы планируете использовать **готовый щит автоматики** с прозрачным пластиковым пластроном, или будете собирать элементы на **уже имеющейся металлической DIN-рейке** в старом распределительном шкафу?
</FollowUp>


