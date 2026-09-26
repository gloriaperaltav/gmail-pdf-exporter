#!/usr/bin/env python3
import json
from jinja2 import Template
from weasyprint import HTML, CSS
from io import BytesIO

correos_data = [
    {"num": 1, "asunto": "[Sentry] KERNEL-BACKEND-WR - TimeoutError", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Sábado, 26 Sep 2026, 01:29:20 UTC", "adjuntos": False, "contenido": "Error timeout en workflow-engine. Celery task falló esperando respuesta. run_agent_llm fue cancelado por timeout tras 380 segundos. Tags: area=workflow-engine, environment=development, level=error."},
    {"num": 2, "asunto": "[Sentry] KERNEL-BACKEND-WQ - TimeLimitExceeded", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Sábado, 26 Sep 2026, 00:27:24 UTC", "adjuntos": False, "contenido": "Celery worker excedió el límite de tiempo (900 segundos / 15 min). Traceback de billiard.exceptions.TimeLimitExceeded. Tags: environment=development, level=error."},
    {"num": 3, "asunto": "[Sentry] KERNEL-FRONTEND-P9 - TypeError: Failed to fetch", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Sábado, 26 Sep 2026, 00:25:54 UTC", "adjuntos": False, "contenido": "Error de fetch fallido en dev.app.getkrnl.ai (chat-stream area). Ocurrió al reanudar stream. Tags: browser=Chrome 154, url=https://dev.app.getkrnl.ai/es/chat, user.role=Super Admin."},
    {"num": 4, "asunto": "[Sentry] KERNEL-BACKEND-WP - Connection to Redis lost", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Sábado, 26 Sep 2026, 00:21:47 UTC", "adjuntos": False, "contenido": "Pérdida de conexión a Redis: 'Connection to Redis lost: Retry (1/20) in 1.00 second.' Environment: production. Tags: component=workflows, level=error."},
    {"num": 5, "asunto": "[Sentry] KERNEL-FRONTEND-P8 - AxiosError: No se pudo completar", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Sábado, 26 Sep 2026, 00:20:05 UTC", "adjuntos": False, "contenido": "Error de axios GET 500 en área de interfaz frontend. Ocurrió en /es/workspace/workflows/new. Tags: http.status_code=500, user.role=Super Admin, environment=development."},
    {"num": 6, "asunto": "[Sentry] KERNEL-BACKEND-WN - OperationalError: connection failed", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Sábado, 26 Sep 2026, 00:13:26 UTC", "adjuntos": False, "contenido": "Falló conexión a base de datos PostgreSQL en 10.100.101.132:5432. 'FATAL: server login has been failing, cached error: connect failed (server_login_retry).' Tags: component=workflows, view=WorkflowViewSet."},
    {"num": 7, "asunto": "[Sentry] KERNEL-FRONTEND-P6 - AxiosError: No se pudo completar", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Viernes, 25 Sep 2026, 23:49:21 UTC", "adjuntos": False, "contenido": "Error de axios POST 500 en endpoint /api/auth/google/. Environment: production. Tags: http.method=POST, http.status_code=500, transaction=/auth/google/callback."},
    {"num": 8, "asunto": "[Sentry] KERNEL-BACKEND-WM - MasterNotFoundError", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Viernes, 25 Sep 2026, 23:49:19 UTC", "adjuntos": False, "contenido": "Redis MasterNotFoundError: 'No master found for mymaster'. Falló durante invalidate_user_model_cache. Tags: component=auth, environment=production, view=GoogleAuthView."},
    {"num": 9, "asunto": "[Sentry] KERNEL-BACKEND-WK - TemplateRenderError", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Viernes, 25 Sep 2026, 23:22:26 UTC", "adjuntos": False, "contenido": "Error en renderización de template: 'expected name or number'. Falló en render_value_isolated(). Tags: component=workflows.execute_workflow_run, environment=development."},
    {"num": 10, "asunto": "[Sentry] KERNEL-BACKEND-WJ - ValueError: JSON inválido", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Viernes, 25 Sep 2026, 23:16:40 UTC", "adjuntos": False, "contenido": "Error al parsear JSON en run_data_parse_json: 'Expecting property name enclosed in double quotes: line 1 column 2'. Tags: component=workflows.execute_workflow_run, environment=development."},
    {"num": 11, "asunto": "[Sentry] KERNEL-BACKEND-WH - TimeoutError", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Viernes, 25 Sep 2026, 22:49:29 UTC", "adjuntos": False, "contenido": "Timeout similar a #1, en workflow-engine. CancelledError seguido de TimeoutError en asyncio.wait_for(). Tags: area=workflow-engine, environment=development."},
    {"num": 12, "asunto": "[Sentry] KERNEL-BACKEND-WG - RuntimeError: Error interno", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Viernes, 25 Sep 2026, 21:59:23 UTC", "adjuntos": False, "contenido": "'Error interno del sistema. Intente nuevamente.' Falló en run_agent_llm. Tags: component=workflows.execute_workflow_run, environment=development."},
    {"num": 13, "asunto": "[Sentry] KERNEL-BACKEND-WF - RuntimeError: HTTP 400", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Viernes, 25 Sep 2026, 21:21:45 UTC", "adjuntos": False, "contenido": "Error HTTP 400 en run_action_http: 'HTTP 400: <!DOCTYPE html>... Bad Request'. Environment: production. Tags: component=workflows.execute_workflow_run."},
    {"num": 14, "asunto": "[Sentry] KERNEL-BACKEND-WE - OperationalError: connection timeout", "remitente": "Sentry Orion", "email": "sentry@cloud.orion.global", "fecha": "Viernes, 25 Sep 2026, 19:03:32 UTC", "adjuntos": False, "contenido": "'connection timeout expired' en PostgreSQL durante autenticación JWT. Environment: qa-salfagpt. Tags: component=skills, server=app-orion-django-langraph-backend-salfagpt-krnl-qa."},
    {"num": 15, "asunto": "Re: [orion-global/django-langraph] Bug OneDrive (Issue #564)", "remitente": "Grecia Gonzalez", "email": "notifications@github.com", "fecha": "Viernes, 25 Sep 2026, 11:19:56 -0700", "adjuntos": False, "contenido": "Fix listo en fix/langraph564. Verificado en local con Gemini 2.5 Flash: El asistente de Microsoft ya carga todas sus herramientas. Excel: texto, número, fórmula y booleano quedan con su tipo correcto. Cambio de comportamiento: al escribir en Excel, una celda vacía (null) se rechaza."},
    {"num": 16, "asunto": "Documento con firma electrónica listo", "remitente": "Gloria Peralta Villasante", "email": "esignature-noreply@google.com", "fecha": "Viernes, 25 Sep 2026, 10:37:24 -0700", "adjuntos": True, "contenido": "Firma electrónica completada. Se ha adjuntado una copia del documento firmado. Se almacena en tu Google Drive. Documento: OP-P&S-FO-12 Consentimiento Informado de Ingreso al PROGRAMA DE PREVENCIÓN DEL ESTRÉS EN EL ÁMBITO LABORAL (1) - 25/9/26, 12:36.pdf (288.7 KB)"},
    {"num": 17, "asunto": "Solicitud de firma electrónica completada", "remitente": "Gloria Peralta Villasante", "email": "esignature-noreply@google.com", "fecha": "Viernes, 25 Sep 2026, 10:37:19 -0700", "adjuntos": False, "contenido": "Firma electrónica completada. Gloria Peralta Villasante (gloria.peralta@orion.global) ha completado la solicitud de firma electrónica de este documento."},
    {"num": 18, "asunto": "Solicitud de firma electrónica (nueva)", "remitente": "Gloria Peralta Villasante", "email": "esignature-noreply@google.com", "fecha": "Viernes, 25 Sep 2026, 10:36:29 -0700", "adjuntos": False, "contenido": "Nueva solicitud de firma electrónica. Has solicitado una firma electrónica en este documento."},
    {"num": 19, "asunto": "Conoce a los miembros del CIFHS 🛡️", "remitente": "Comunicaciones Internas", "email": "comunicaciones_internas@orion.global", "fecha": "Viernes, 25 Sep 2026, 12:11:51 -0500", "adjuntos": True, "contenido": "¿Conocen a los miembros del Comité de Intervención Frente al Hostigamiento Sexual (CIFHS) para el periodo 2026-2028? ¡Aquí se los presentamos! Pueden ver el organigrama completo con todos los integrantes en la imagen adjunta (COMITE HST_page-0001.jpg - 480.9 KB)"},
    {"num": 20, "asunto": "What Stage Is Your Project? Takeaways For AI Engineering", "remitente": "The Batch @ DeepLearning.AI", "email": "thebatch@deeplearning.ai", "fecha": "Viernes, 25 Sep 2026, 08:25:10 -0700", "adjuntos": False, "contenido": "Opus Stalks the Frontier, Jev Classifies Everything, Running Two Agents at Once... Moving forward on early stage, 0-to-1 projects and mature projects requires very different tactics. For those who aspire to be skilled at AI Engineering, I've found that selecting the right tactic based on stage of project is one of the hardest but most important things to learn."}
]

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Exportación de Correos Gmail</title>
    <style>
        * { margin: 0; padding: 0; }
        @page { size: A4; margin: 2cm; @bottom-center { content: "Página " counter(page) " de " counter(pages); } }
        body { font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: #333; line-height: 1.6; }
        .portada { page-break-after: always; text-align: center; padding: 5cm 0; display: flex; flex-direction: column; justify-content: center; min-height: 100vh; }
        .portada h1 { font-size: 48px; color: #1a3a52; margin-bottom: 1cm; font-weight: 700; }
        .portada p { font-size: 16px; color: #666; margin: 0.3cm 0; }
        .indice { page-break-after: always; }
        .indice h2 { font-size: 28px; color: #1a3a52; margin-bottom: 1cm; }
        .indice-item { font-size: 12px; margin: 0.4cm 0; padding-left: 0.5cm; color: #1a3a52; }
        .correo { page-break-inside: avoid; margin-bottom: 1.2cm; padding: 0.8cm; border-left: 4px solid #1a3a52; background: #f9fafb; }
        .correo h3 { font-size: 16px; color: #1a3a52; margin-bottom: 0.5cm; font-weight: 600; }
        .correo-meta { font-size: 11px; color: #555; margin-bottom: 0.3cm; }
        .correo-contenido { font-size: 12px; color: #333; margin-top: 0.5cm; line-height: 1.5; }
    </style>
</head>
<body>
    <div class="portada">
        <h1>Exportación de Correos Gmail</h1>
        <p>gloria.peralta@orion.global</p>
        <p>26 de septiembre de 2026</p>
        <div style="margin-top: 2cm;">
            <p style="font-size: 14px; color: #555;">Total de correos: {{ correos|length }}</p>
        </div>
    </div>

    <div class="indice">
        <h2>Índice de Correos</h2>
        {% for correo in correos %}
        <div class="indice-item">{{ correo.num }}. {{ correo.asunto }}</div>
        {% endfor %}
    </div>

    {% for correo in correos %}
    <div class="correo">
        <h3>Correo #{{ correo.num }}: {{ correo.asunto }}</h3>
        <div class="correo-meta">
            <div><strong>De:</strong> {{ correo.remitente }} &lt;{{ correo.email }}&gt;</div>
            <div><strong>Fecha:</strong> {{ correo.fecha }}</div>
            <div><strong>Adjuntos:</strong> {% if correo.adjuntos %}Sí{% else %}No{% endif %}</div>
        </div>
        <div class="correo-contenido">{{ correo.contenido }}</div>
    </div>
    {% endfor %}
</body>
</html>
"""

try:
    html_content = Template(html_template).render(correos=correos_data)
    HTML(string=html_content).write_pdf('correos_gmail.pdf')
    print("✓ PDF generado: correos_gmail.pdf")
    print(f"✓ Total: {len(correos_data)} correos")
except Exception as e:
    print(f"Error: {e}")
