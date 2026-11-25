---
name: matlab-app-design
description: How to build and test a MATLAB app as a uifigure with an HTML panel and a clean design. Use when making a graphical interface.
---

# Building a MATLAB app with an HTML screen

The app is a `uifigure` holding one `uihtml` component. The screen is
HTML, CSS and JavaScript; the numbers are MATLAB. You cannot see the
window, so the app is built to be driven and photographed from a script.
Checked on R2024a. If the project has its own style guide or coding
standard, it wins over this guide.

## 1. Three layers, three places

```
MyTool.m                      app class: window, state, messages
business_logic/               computing; takes arrays, returns arrays
ui/my_tool.html (.css, .js)   the screen; draws what MATLAB sends
tests/
```

- **Logic knows nothing about the window.** It takes data, not file
  names or handles; it raises errors with identifiers and the app class
  turns them into a message on screen. No dialogs inside logic.
- **MATLAB holds the state** (data, parameters, results). The page shows
  what it is sent and reports what the person did; it keeps no second
  copy of the truth.
- HTML, CSS and JavaScript live in their own files, not in long strings
  inside MATLAB code.

## 2. The window

```matlab
root = fileparts(mfilename('fullpath'));
fig = uifigure('Visible', 'off', 'Name', 'My tool', 'Position', [100 100 1280 800]);
fig.CloseRequestFcn = @(~, ~) onClose();
g = uigridlayout(fig, [1 1], 'Padding', 0);
h = uihtml(g, 'HTMLSource', fullfile(root, 'ui', 'my_tool.html'));
h.DataChangedFcn = @(src, ~) onAction(src.Data);
fig.Visible = 'on';
```

Create it hidden and show it when it is ready. The path to the page comes
from the file's own location. The close callback stops timers and deletes
the figure, also after an error.

## 3. Messages between page and MATLAB

```javascript
function setup(htmlComponent) {
  htmlComponent.addEventListener("DataChanged", () => render(htmlComponent.Data));
  document.getElementById("run").addEventListener("click", () => {
    htmlComponent.Data = { source: "html", action: "run", n: ++counter, params: readForm() };
  });
}
```

```matlab
counter = counter + 1;
h.Data = struct('source', 'matlab', 'kind', 'state', 'n', counter, 'state', publicState);
```

- MATLAB calls `setup` once the page has loaded, 3 to 7 seconds after
  the window is created. A value set before that is still in `Data`
  when `setup` runs, but only the last one: have the page say it is
  ready and send the first state in answer.
- **The same value twice is not delivered.** Setting `Data` to something
  identical to the last value fires no event (three equal assignments,
  one event), so a second click on the same button would do nothing.
  Every message carries a counter.
- **Assignments made in a row are merged.** Setting `Data` to 7, 8 and 9
  without a pause reached the page as one event holding 9. `Data` is a
  state, not a queue: send the whole current state in one message, and
  use events (below) for things that must each arrive.
- Setting `Data` from MATLAB does not call MATLAB's own
  `DataChangedFcn`; it fires only for changes made by the page. Both
  sides still read the same property, so mark who sent each message
  (`source`) and ignore your own.
- `htmlComponent.sendEventToMATLAB('Name', data)` with
  `HTMLEventReceivedFcn` is the other channel, for events that are not
  state.
- One action name per thing the person can do (`load`, `set_params`,
  `run`, `export`). Check every field that arrives from the page before
  using it, as for any input.

## 4. Every click also has a function

`onAction` only unpacks the message and calls a method (`app.run()`,
`app.setParams(p)`, `app.loadMatrix(X)`). The same methods are public, so
a script can load known data, change parameters, run and export with no
mouse and no file dialog. That is what makes the app testable, and it
lets the person automate it later.

- File and folder pickers stay at the edge: the button calls the picker
  and then the method that takes a path. The method is what tests call.
- Loading from the base workspace and sending results back to it
  (`evalin`, `assignin`) is a normal request for an app. Show the names
  that will be created, and do not replace a variable that exists unless
  the person says so.
- Long computations: show that work is in progress, send progress
  messages, and leave a way to stop. A frozen window with no sign reads
  as a crash.

## 5. The page

- `html, body { height: 100%; margin: 0; }` or the background covers only
  the strip the content occupies.
- All colours, sizes and spacings as CSS variables in one place; the
  default values are in [style](references/style.md). No colour written
  inside a rule, no inline styles.
- Plots drawn in the page (a `canvas` sized by the device pixel ratio)
  respond at once to zoom and selection; send them the numbers they
  draw, thinned to what the screen can show, not the whole data set.
- Everything the app needs is in its folder: no fonts, scripts or styles
  fetched from the internet, so it works offline and in ten years.
- Each control has a visible text label, a state for hover, focus and
  disabled, and works from the keyboard. Errors say what happened and
  what to do, next to where they happened.
- Empty states: before data is loaded the screen says what to do first.

## 6. Look at it

```matlab
app = MyTool();
t = tic;  while ~app.PageReady && toc(t) < 20, pause(0.2); end   % set by the page's "ready" message
app.loadMatrix(X);  app.run();  pause(1);
exportapp(app.UIFigure, 'after_run.png');
```

The page took 3 to 7 seconds to load: wait for its ready message with a
time limit, not for a fixed pause. `exportapp` works with the figure
hidden, but **the picture does not show values that JavaScript put into
form fields** (`input.value`, the chosen option of a `select`): they
come out empty or at their HTML default. When the page sets a field,
have it set the attribute too (`setAttribute('value', v)`, `selected`),
or have the page report its field values in a message and check those.
Take a picture of each state
that matters (empty, loaded, running, result, error, the narrowest
width supported), **open each picture and look at it**: text cut off,
overlapping panels, a blank area, a plot with no axis. Then compare the
numbers the app shows with the same computation called directly on the
logic. Clicks themselves cannot be made from a script: say which
interactions only the person can try, and ask them to.

## 7. What to hand back

How to start the app, the script that drives it and its pictures, what
was compared against a direct computation, the interactions left for the
person to try, and the licence and citation shown in the app's header
(matlab-writing-code skill).
