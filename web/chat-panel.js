/* 한입뉴스 AI 어시스턴트 채팅 패널
 * API 서버: api/server.js (기본 http://localhost:3001)
 * window.CHAT_API_URL 로 오버라이드 가능 */
(function () {
  'use strict';

  const API_BASE = (window.CHAT_API_URL || 'http://localhost:3001').replace(/\/$/, '');

  /* ── DOM 생성 ───────────────────────────────────────── */
  function buildDOM() {
    /* 오버레이 */
    const overlay = el('div', { id: 'cp-overlay' });

    /* 패널 */
    const panel = el('div', { id: 'cp-panel', role: 'dialog', 'aria-label': 'AI 어시스턴트', 'aria-modal': 'true' });
    panel.innerHTML = `
      <div id="cp-header">
        <div id="cp-header-left">
          <svg id="cp-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/>
            <path d="M12 6v6l4 2"/>
          </svg>
          <span id="cp-title">AI 어시스턴트</span>
        </div>
        <button id="cp-close" aria-label="패널 닫기">✕</button>
      </div>
      <div id="cp-context-bar"></div>
      <div id="cp-messages" role="log" aria-live="polite"></div>
      <div id="cp-input-area">
        <textarea id="cp-input" placeholder="궁금한 점을 물어보세요… (Enter 전송, Shift+Enter 줄바꿈)" rows="1" aria-label="질문 입력"></textarea>
        <button id="cp-send" aria-label="전송">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>`;

    /* 트리거 버튼 */
    const trigger = el('button', { id: 'cp-trigger', 'aria-label': 'AI 어시스턴트 열기' });
    trigger.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
      AI 질문`;

    document.body.appendChild(overlay);
    document.body.appendChild(panel);
    document.body.appendChild(trigger);
    return { overlay, panel, trigger };
  }

  function el(tag, attrs) {
    const e = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => e.setAttribute(k, v));
    return e;
  }

  /* ── 기사 컨텍스트 자동 추출 ─────────────────────────── */
  function getArticleContext() {
    const titleEl = document.querySelector('h1.article-title, h1.stock-title, .article-header h1, h1');
    const title = titleEl?.textContent?.trim() || document.title.replace(' — 병규의 한입뉴스', '').trim();

    const bodyEl = document.querySelector('.article-body, .stock-card-body, .stock-analysis');
    const summary = bodyEl
      ? bodyEl.innerText.replace(/\s+/g, ' ').trim().slice(0, 600)
      : '';

    return { title, summary };
  }

  /* ── 메시지 렌더링 ──────────────────────────────────── */
  function appendMsg(container, role, html) {
    const wrap = el('div', { class: `cp-msg cp-msg-${role}` });
    const bubble = el('div', { class: 'cp-bubble' });
    bubble.innerHTML = html;
    wrap.appendChild(bubble);
    container.appendChild(wrap);
    container.scrollTop = container.scrollHeight;
    return wrap;
  }

  function md2html(text) {
    return text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
      .replace(/\n/g, '<br>');
  }

  function showTyping(container) {
    const wrap = el('div', { class: 'cp-msg cp-msg-ai', id: 'cp-typing' });
    wrap.innerHTML = '<div class="cp-bubble cp-dots"><span></span><span></span><span></span></div>';
    container.appendChild(wrap);
    container.scrollTop = container.scrollHeight;
  }

  /* ── API 호출 ───────────────────────────────────────── */
  async function callAPI(messages, ctx) {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages, articleContext: ctx }),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.error || `HTTP ${res.status}`);
    }
    return (await res.json()).reply;
  }

  /* ── 초기화 ─────────────────────────────────────────── */
  function init() {
    const { overlay, panel, trigger } = buildDOM();
    const msgsEl  = panel.querySelector('#cp-messages');
    const inputEl = panel.querySelector('#cp-input');
    const sendBtn = panel.querySelector('#cp-send');
    const closeBtn = panel.querySelector('#cp-close');
    const ctxBar  = panel.querySelector('#cp-context-bar');

    const history = [];   /* { role, content } */
    let isOpen    = false;
    let sending   = false;

    /* 컨텍스트 표시 */
    const ctx = getArticleContext();
    if (ctx.title) {
      ctxBar.textContent = `📄 ${ctx.title}`;
      ctxBar.style.display = 'block';
    }

    /* 열기 */
    function open() {
      isOpen = true;
      panel.classList.add('cp-open');
      overlay.classList.add('cp-show');
      document.body.classList.add('cp-body-shift');
      inputEl.focus();
      if (history.length === 0) {
        appendMsg(msgsEl, 'ai',
          '안녕하세요! 기사에 대해 궁금한 점을 물어보세요.<br>' +
          '웹 검색을 통해 최신 정보로 답변해드릴게요. 😊');
      }
    }

    /* 닫기 */
    function close() {
      isOpen = false;
      panel.classList.remove('cp-open');
      overlay.classList.remove('cp-show');
      document.body.classList.remove('cp-body-shift');
    }

    trigger.addEventListener('click', open);
    closeBtn.addEventListener('click', close);
    overlay.addEventListener('click', close);
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && isOpen) close(); });

    /* 메시지 전송 */
    async function send() {
      const text = inputEl.value.trim();
      if (!text || sending) return;

      sending = true;
      sendBtn.disabled = true;
      inputEl.value = '';
      autoResize();

      appendMsg(msgsEl, 'user', md2html(text));
      history.push({ role: 'user', content: text });
      showTyping(msgsEl);

      try {
        const reply = await callAPI(
          history.map(m => ({ role: m.role, content: m.content })),
          ctx
        );
        document.getElementById('cp-typing')?.remove();
        appendMsg(msgsEl, 'ai', md2html(reply));
        history.push({ role: 'assistant', content: reply });
      } catch (err) {
        document.getElementById('cp-typing')?.remove();
        const isNet = /fetch|network|ECONNREFUSED/i.test(err.message);
        appendMsg(msgsEl, 'ai',
          isNet
            ? '⚠️ AI 서버에 연결할 수 없습니다.<br>' +
              '<code>cd api &amp;&amp; npm install &amp;&amp; npm start</code><br>' +
              '명령으로 서버를 실행해주세요.'
            : `⚠️ 오류: ${md2html(err.message)}`
        );
      } finally {
        sending = false;
        sendBtn.disabled = false;
        inputEl.focus();
      }
    }

    sendBtn.addEventListener('click', send);
    inputEl.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
    });

    /* textarea 자동 높이 */
    function autoResize() {
      inputEl.style.height = 'auto';
      inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + 'px';
    }
    inputEl.addEventListener('input', autoResize);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
