# -*- coding: utf-8 -*-
main_hero = '(🌟Поздравляем! Новый уровень!🌟\\n' \
            'Жми /level_up\\n\\n)?' \
            'Битва пяти замков через (?:([0-9]+)ч)?(?: ([0-9]+) минут!)?(?:.*)?\\n\\n' \
            '(🇬🇵|🇮🇲|🇨🇾|🇻🇦|🇪🇺)(.+), (.+) .+ замка\\n' \
            '🏅Уровень: ([0-9]+)\\n' \
            '(?:.*)Атака: ([0-9]+) 🛡Защита: ([0-9]+)\\n' \
            '🔥Опыт: ([0-9]+)/([0-9]+)\\n' \
            '🔋Выносливость: ([0-9]+)/([0-9]+)\\n' \
            '💰([0-9]+) 💠([0-9]+)\\n\\n' \
            '🎽Экипировка (.+)\\n' \
            '🎒Рюкзак: ([0-9]+)/([0-9]+) /inv' \
            '(?:\\n\\nПитомец:\\n(.+?) (?:.+?) (.+)? \(([0-9]+) ур\.\) (.+) /pet)?' \
            '\\n\\nСостояние:\\n(.+)' \
            '\\n\\nПодробнее: /hero'

captcha = '(?:(На выходе из замка охрана никого не пропускает.*)|' \
          'Не умничай! Отвечай одним из предложенных вариантов|' \
          'Не шути со стражниками! Отвечай одним из предложенных вариантов)'

uncaptcha = 'Ты ответил правильно, приключения ждут!'