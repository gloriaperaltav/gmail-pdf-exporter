# Gmail PDF Exporter

Script para exportar correos de Gmail a un PDF profesional con portada e índice.

## Requisitos

```bash
pip install jinja2 weasyprint
```

## Uso

```bash
python3 generate_pdf.py
```

## Salida

Genera un archivo `correos_gmail.pdf` con:
- ✓ Portada profesional
- ✓ Índice de correos
- ✓ 20 correos con información completa (remitente, fecha, contenido, adjuntos)
- ✓ Numeración de páginas
- ✓ Estilos profesionales

## Características

- **Portada**: Título, email y fecha
- **Índice**: Lista de todos los correos
- **Correos**: Información detallada de cada uno
- **Paginación**: Numeración automática de páginas
- **Responsive**: Diseño adaptado para impresión en A4

## Salida esperada

```
✓ PDF generado: correos_gmail.pdf
✓ Total: 20 correos
```
