import { transformWithPlugins } from "./babel-utils.js";
import { createServer, send } from "./mq.js";

const PADDING_CHARS = 400;

export const localReanme = () => {
  createServer();

  return async (code: string): Promise<string> => {
    let didChange = false;
    let newCode = code;
    let pos = 0;
    do {
      didChange = false;
      newCode = await transformWithPlugins(newCode, [
        {
          visitor: {
            Identifier(path) {
              if (didChange) return;
              if (path.node.name.length >= 3) return;
              const start = path.node.start ?? newCode.length;
              if (start <= pos) return;

              const { renamed } = send<{ renamed: string }>({
                type: "rename",
                before: newCode.slice(
                  Math.max(start - PADDING_CHARS, 0),
                  start
                ),
                after: newCode.slice(start, start + PADDING_CHARS),
              });
              console.log(renamed);
              path.scope.rename(path.node.name, renamed);
              didChange = true;
              pos = start;
            },
          },
        },
      ]);
      console.log(Math.round((pos / newCode.length) * 1000) / 10 + "%");
    } while (didChange);
    return newCode;
  };
};
