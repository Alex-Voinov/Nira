// Для CSS модулей
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

// Для SCSS/SASS модулей
declare module '*.module.scss' {
  const classes: { [key: string]: string };
  export default classes;
}