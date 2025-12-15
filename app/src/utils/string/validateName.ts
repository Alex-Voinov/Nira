const USERNAME_MIN_LENGTH = 2;
const USERNAME_MAX_LENGTH = 20;

const validateName = (name: string) => {
  const trimmed = name.trim()

  // 1. Длина
  if (trimmed.length < USERNAME_MIN_LENGTH)
    return "Слишком короткое имя"

  if (trimmed.length > USERNAME_MAX_LENGTH)
    return `Максимальная длина — ${USERNAME_MAX_LENGTH} символов`

  // 2. Только один пробел
  const spaceCount = [...trimmed].filter(ch => ch === " ").length
  if (spaceCount > 1)
    return "Можно использовать максимум один пробел"

  // 3. Цифры запрещены
  if (/\d/.test(trimmed))
    return "Имя не должно содержать цифры"

  // 4. Только русский или только английский
  const isRussian = /^[А-Яа-яЁё ]+$/.test(trimmed)
  const isEnglish = /^[A-Za-z ]+$/.test(trimmed)

  if (!isRussian && !isEnglish)
    return "Имя должно быть только на русском или только на английском"
}

export default validateName;