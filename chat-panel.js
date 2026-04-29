/* 한입뉴스 AI 어시스턴트 — 브라우저 직접 호출 방식
 * API 키는 localStorage에 저장 (한 번만 입력) */
(function () {
  'use strict';

  const ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages';
  const MODEL         = 'claude-haiku-4-5-20251001';
  const LS_KEY        = 'hanip_anthropic_key';

  /* ── DOM 생성 ───────────────────────────────────────── */
  function buildDOM() {
    const overlay = el('div', { id: 'cp-overlay' });

    const panel = el('div', {
      id: 'cp-panel',
      role: 'dialog',
      'aria-label': 'AI 어시스턴트',
      'aria-modal': 'true',
    });
    panel.innerHTML = `
      <div id="cp-header">
        <div id="cp-header-left">
          <svg id="cp-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          <span id="cp-title">AI 어시스턴트</span>
        </div>
        <div style="display:flex;align-items:center;gap:6px;">
          <button id="cp-key-btn" title="API 키 변경" aria-label="API 키 변경">🔑</button>
          <button id="cp-close" aria-label="패널 닫기">✕</button>
        </div>
      </div>
      <div id="cp-context-bar"></div>

      <!-- API 키 입력 화면 -->
      <div id="cp-key-screen">
        <div id="cp-key-inner">
          <div id="cp-key-icon">🔑</div>
          <p id="cp-key-title">Anthropic API 키 입력</p>
          <p id="cp-key-desc">
            키는 브라우저에만 저장되며 외부로 전송되지 않습니다.<br>
            <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener">console.anthropic.com</a>에서 발급하세요.
          </p>
          <input id="cp-key-input" type="password" placeholder="sk-ant-api03-..." autocomplete="off" spellcheck="false"/>
          <button id="cp-key-save">저장하고 시작하기</button>
          <p id="cp-key-error"></p>
        </div>
      </div>

      <!-- 채팅 화면 -->
      <div id="cp-chat-screen" style="display:none;flex:1;flex-direction:column;overflow:hidden;">
        <div id="cp-messages" role="log" aria-live="polite"></div>
        <div id="cp-input-area">
          <textarea id="cp-input" placeholder="궁금한 점을 물어보세요… (Enter 전송, Shift+Enter 줄바꿈)" rows="1" aria-label="질문 입력"></textarea>
          <button id="cp-send" aria-label="전송">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </div>
      </div>`;

    const trigger = el('button', { id: 'cp-trigger', 'aria-label': 'AI 어시스턴트 열기' });
    trigger.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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

  /* ── 기사 컨텍스트 추출 ─────────────────────────────── */
  function getArticleContext() {
    const titleEl = document.querySelector('h1.article-title, .article-header h1, h1');
    const title   = titleEl?.textContent?.trim() || document.title.replace(' — 병규의 한입뉴스', '').trim();
    const bodyEl  = document.querySelector('.article-body, .stock-card-body, .stock-analysis');
    const summary = bodyEl ? bodyEl.innerText.replace(/\s+/g, ' ').trim().slice(0, 600) : '';
    return { title, summary };
  }

  /* ── 메시지 렌더링 ──────────────────────────────────── */
  function appendMsg(container, role, html) {
    const wrap   = el('div', { class: `cp-msg cp-msg-${role}` });
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

  /* ── Anthropic API 직접 호출 ────────────────────────── */
  async function callAnthropic(messages, ctx, apiKey) {
    const systemParts = [
      '당신은 "병규의 한입뉴스"의 AI 어시스턴트입니다.',
      '과학기술, AI, 경제·주식 뉴스 기사에 관한 독자의 질문에 답변합니다.',
      '답변은 간결하고 명확하게 한국어로 작성하세요.',
      '전문 용어가 처음 등장할 때는 괄호 안에 간단히 설명하세요.',
    ];
    if (ctx?.title)   systemParts.push(`\n현재 독자가 읽고 있는 기사: "${ctx.title}"`);
    if (ctx?.summary) systemParts.push(`기사 내용 일부:\n${ctx.summary}`);

    const res = await fetch(ANTHROPIC_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true',
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 1024,
        system: systemParts.join('\n'),
        messages,
      }),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      const msg  = body.error?.message || `HTTP ${res.status}`;
      throw new Error(msg);
    }

    const data = await res.json();
    return data.content?.find(c => c.type === 'text')?.text || '응답을 생성하지 못했습니다.';
  }

  /* ── 초기화 ─────────────────────────────────────────── */
  function init() {
    const { overlay, panel, trigger } = buildDOM();

    const keyScreen  = panel.querySelector('#cp-key-screen');
    const chatScreen = panel.querySelector('#cp-chat-screen');
    const keyInput   = panel.querySelector('#cp-key-input');
    const keySaveBtn = panel.querySelector('#cp-key-save');
    const keyError   = panel.querySelector('#cp-key-error');
    const keyBtn     = panel.querySelector('#cp-key-btn');
    const msgsEl     = panel.querySelector('#cp-messages');
    const inputEl    = panel.querySelector('#cp-input');
    const sendBtn    = panel.querySelector('#cp-send');
    const closeBtn   = panel.querySelector('#cp-close');
    const ctxBar     = panel.querySelector('#cp-context-bar');

    const history = [];
    let isOpen    = false;
    let sending   = false;

    /* 컨텍스트 표시 */
    const ctx = getArticleContext();
    if (ctx.title) {
      ctxBar.textContent  = `📄 ${ctx.title}`;
      ctxBar.style.display = 'block';
    }

    /* 화면 전환 */
    function showKeyScreen() {
      keyScreen.style.display  = 'flex';
      chatScreen.style.display = 'none';
      keyBtn.style.display     = 'none';
      setTimeout(() => keyInput.focus(), 50);
    }
    function showChatScreen() {
      keyScreen.style.display  = 'none';
      chatScreen.style.display = 'flex';
      keyBtn.style.display     = 'block';
      if (history.length === 0) {
        appendMsg(msgsEl, 'ai',
          '안녕하세요! 기사에 대해 궁금한 점을 물어보세요. 😊<br>' +
          '<span style="font-size:12px;color:#64748B;">Claude의 학습 지식 기반으로 답변합니다.</span>');
      }
      setTimeout(() => inputEl.focus(), 50);
    }

    /* 열기/닫기 */
    function open() {
      isOpen = true;
      panel.classList.add('cp-open');
      overlay.classList.add('cp-show');
      document.body.classList.add('cp-body-shift');
      const saved = localStorage.getItem(LS_KEY);
      saved ? showChatScreen() : showKeyScreen();
    }
    function close() {
      isOpen = false;
      panel.classList.remove('cp-open');
      overlay.classList.remove('cp-show');
      document.body.classList.remove('cp-body-shift');
    }

    trigger.addEventListener('click', open);
    closeBtn.addEventListener('click', close);
    overlay.addEventListener('click', close);
    keyBtn.addEventListener('click', showKeyScreen);
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && isOpen) close(); });

    /* API 키 저장 */
    function saveKey() {
      const key = keyInput.value.trim();
      if (!key.startsWith('sk-ant-')) {
        keyError.textContent = '올바른 API 키 형식이 아닙니다 (sk-ant-... 로 시작해야 합니다).';
        return;
      }
      localStorage.setItem(LS_KEY, key);
      keyError.textContent = '';
      keyInput.value       = '';
      showChatScreen();
    }
    keySaveBtn.addEventListener('click', saveKey);
    keyInput.addEventListener('keydown', e => { if (e.key === 'Enter') saveKey(); });

    /* 메시지 전송 */
    async function send() {
      const text   = inputEl.value.trim();
      const apiKey = localStorage.getItem(LS_KEY);
      if (!text || sending) return;
      if (!apiKey) { showKeyScreen(); return; }

      sending = true;
      sendBtn.disabled = true;
      inputEl.value    = '';
      autoResize();

      appendMsg(msgsEl, 'user', md2html(text));
      history.push({ role: 'user', content: text });
      showTyping(msgsEl);

      try {
        const reply = await callAnthropic(
          history.map(m => ({ role: m.role, content: m.content })),
          ctx,
          apiKey
        );
        document.getElementById('cp-typing')?.remove();
        appendMsg(msgsEl, 'ai', md2html(reply));
        history.push({ role: 'assistant', content: reply });
      } catch (err) {
        document.getElementById('cp-typing')?.remove();
        const isAuth = /unauthorized|api.key|credit|balance/i.test(err.message);
        if (isAuth) {
          appendMsg(msgsEl, 'ai',
            '⚠️ API 키가 유효하지 않거나 크레딧이 부족합니다.<br>' +
            '🔑 버튼을 눌러 키를 다시 입력하거나, ' +
            '<a href="https://console.anthropic.com/settings/billing" target="_blank" rel="noopener">크레딧을 충전</a>해주세요.');
        } else {
          appendMsg(msgsEl, 'ai', `⚠️ 오류: ${md2html(err.message)}`);
        }
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
