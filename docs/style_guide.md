# Jumping Ball Game Style Guide

## Color Palette

### Primary Colors
- **Background Blue (Main Menu)**: `(50, 100, 150)`
- **Background Blue (Map Selection)**: `(70, 120, 170)`
- **Background Blue (Official Maps)**: `(60, 110, 160)`
- **Background Blue (Settings)**: `(60, 80, 140)`
- **Background Blue (How to Play)**: `(40, 90, 130)`
- **Background Blue (Custom Maps)**: `(50, 70, 120)`
- **Dark Background (Game Over)**: `(30, 30, 50)`

### UI Element Colors
- **Button Blue**: `(40, 80, 120)`
- **Highlight Red**: `(255, 0, 0)`
- **Text White**: `(255, 255, 255)`
- **Text Black**: `(0, 0, 0)`
- **Success Green**: `(0, 255, 0)`
- **Warning Yellow**: `(255, 255, 0)`
- **Danger Red**: `(255, 0, 0)`

### Platform Colors
- **Regular Platform**: `(0, 255, 0)` (Green)
- **Moving Platform**: `(0, 0, 255)` (Blue)
- **Disappearing Platform**: `(255, 255, 0)` (Yellow)
- **Dangerous Platform**: `(255, 0, 0)` (Red)

## Typography

### Font Families
- System default font (`pygame.font.SysFont(None, size)`)

### Font Sizes
- **Title (Large)**: 72px
- **Title (Medium)**: 64px
- **Header**: 56px
- **Subheader**: 48px
- **Menu Options**: 36px
- **Standard Text**: 32px
- **Small Text**: 24px
- **Footer/Notes**: 20px

## UI Elements

### Buttons
- **Standard Size**: 300px × 100px
- **Border**: 3px white border
- **Text**: Centered, 36px font
- **State Change**: Color shift on selection/hover

### Panels/Boxes
- **Border Radius**: 0px (rectangular design)
- **Border**: 2-3px, white or black depending on context
- **Background**: Semi-transparent or solid color depending on context

### Selection Indicators
- **Menu Arrow**: Red triangle pointing to selected option
- **Selection Highlight**: Red text or outline around selected item
- **Game Over Indicator**: Colored circle (8px radius)

## Layout Guidelines

### Screen Organization
- **Title/Header**: Top portion (60-100px from top)
- **Main Content**: Center portion
- **Footer/Instructions**: Bottom portion (40-50px from bottom)

### Spacing
- **Button Padding**: 40px between major buttons
- **Option Height**: 40px between menu options
- **Section Spacing**: 30-40px between major sections

## Animation Guidelines

### Transitions
- Screen transitions: None currently implemented (future enhancement)

### Interactive Elements
- **Auto-jump Message**: Appears for 2 seconds with fade effect
- **Coming Soon Indicator**: Simple 3-frame animation (500ms per frame)

## Screen-Specific Guidelines

### Main Menu
- Blue gradient background
- Centered title "JUMPING BALL"
- Decorative circles for visual interest
- Centered menu options with selection indicator
- Footer with usage instructions

### Map Selection
- Slightly different blue background from main menu
- Large buttons for Official/Custom maps
- Descriptive text under each option
- Footer with navigation instructions

### Game Over / Level Complete
- Dark background for contrast
- Large title (color depends on outcome)
- Centered score display
- Options with selection indicator
- Decorative horizontal line

### Settings Screen
- Organized in sections: sound, music, controls
- Each setting clearly labeled
- Visual indicators for current state
- Footer with note about future updates

### How to Play Screen
- Organized in sections with clear headers
- Visual examples of game elements
- Concise instructions with bullet points
- Footer with return instructions

## Implementation Notes

- Maintain consistent spacing and alignment across screens
- Use the same background style within screen categories
- Ensure all interactive elements have visual feedback
- Include clear navigation instructions on every screen
- Text should be high contrast and readable 