import { useState } from 'react';
import hljs from 'highlight.js';

import { cn } from '@/lib/utils';

import CopyButton from '@/components/CopyButton';

function CodeBlock({
  language,
  value,
  className,
  codeClass,
  copyable = true,
  codeWrap = false,
  copyOnHover = false,
  noCodeFont = false,
  noMask = true,
}: {
  language: string;
  value: string;
  className?: string;
  codeClass?: string;
  copyable?: boolean;
  codeWrap?: boolean;
  copyOnHover?: boolean;
  noCodeFont?: boolean;
  noMask?: boolean;
}) {
  value = value || '';
  hljs.getLanguage(language) ? (language = language) : (language = 'plaintext');
  const highlightedCode = hljs.highlight(value, { language }).value;
  const [isBlockHovered, setIsBlockHovered] = useState(false);

  return (
    <pre
      className={cn(
        `relative flex w-full overflow-hidden rounded-lg ${
          value ? 'border' : null
        } ${codeWrap ? 'whitespace-pre-wrap' : null} `,
        className
      )}
      onMouseEnter={() => {
        setIsBlockHovered(true);
      }}
      onMouseLeave={() => {
        setIsBlockHovered(false);
      }}
    >
      <CopyButton
        value={value}
        copyable={copyable}
        isBlockHovered={copyOnHover ? isBlockHovered : true}
      />

      {!noMask && (
        <div className='absolute -right-4 top-0 h-full w-12 bg-background blur'></div>
      )}
      <code
        dangerouslySetInnerHTML={{ __html: highlightedCode }}
        className={cn(
          `hljs ${language} no-scrollbar min-w-full overflow-x-scroll  px-4 py-3 text-sm ${
            !noCodeFont ? 'font-mono' : ''
          }`,
          codeClass
        )}
      ></code>
    </pre>
  );
}

export default CodeBlock;
