/**
 * animator.js - Frame-Based Sprite Animation
 * 
 * Simple frame animation system for sprite sheets
 * 
 * Usage:
 *   const idleFrames = [frame0, frame1, frame2, frame3];
 *   const idle = new Animator(idleFrames, 8); // 8 fps
 *   
 *   // In game loop:
 *   idle.update(dt);
 *   const frame = idle.current();
 *   ctx.drawImage(spriteSheet, frame.x, frame.y, frame.w, frame.h, x, y, frame.w, frame.h);
 */

class Animator {
  /**
   * @param {Array} frames - Array of frame data {x, y, w, h} or any frame identifier
   * @param {number} fps - Frames per second
   * @param {boolean} loop - Whether to loop the animation
   */
  constructor(frames, fps = 8, loop = true) {
    this.frames = frames;
    this.fps = fps;
    this.loop = loop;
    this.t = 0;        // Accumulated time
    this.idx = 0;      // Current frame index
    this.finished = false;
  }
  
  /**
   * Update the animator
   * @param {number} dt - Delta time in seconds
   */
  update(dt) {
    if (this.finished) return;
    
    this.t += dt;
    const frameDur = 1 / this.fps;
    
    while (this.t >= frameDur) {
      this.t -= frameDur;
      this.idx++;
      
      if (this.idx >= this.frames.length) {
        if (this.loop) {
          this.idx = 0;
        } else {
          this.idx = this.frames.length - 1;
          this.finished = true;
        }
      }
    }
  }
  
  /**
   * Get the current frame
   * @returns {*} Current frame data
   */
  current() {
    return this.frames[this.idx];
  }
  
  /**
   * Get current frame index
   * @returns {number}
   */
  currentIndex() {
    return this.idx;
  }
  
  /**
   * Reset animation to first frame
   */
  reset() {
    this.t = 0;
    this.idx = 0;
    this.finished = false;
  }
  
  /**
   * Set animation to a specific frame
   * @param {number} index - Frame index
   */
  setFrame(index) {
    this.idx = Math.max(0, Math.min(index, this.frames.length - 1));
    this.t = 0;
  }
  
  /**
   * Check if animation has finished (non-looping only)
   * @returns {boolean}
   */
  isFinished() {
    return this.finished;
  }
}

/**
 * Animation Controller - manages multiple named animations
 * 
 * Usage:
 *   const controller = new AnimationController();
 *   controller.add('idle', new Animator(idleFrames, 8));
 *   controller.add('run', new Animator(runFrames, 12));
 *   controller.add('jump', new Animator(jumpFrames, 10, false));
 *   
 *   controller.play('idle');
 *   
 *   // In game loop:
 *   controller.update(dt);
 *   const frame = controller.current();
 */
class AnimationController {
  constructor() {
    this.animations = new Map();
    this.current = null;
    this.currentName = null;
  }
  
  /**
   * Add an animation
   * @param {string} name - Animation name
   * @param {Animator} animator - Animator instance
   */
  add(name, animator) {
    this.animations.set(name, animator);
    if (!this.current) {
      this.current = animator;
      this.currentName = name;
    }
  }
  
  /**
   * Play an animation
   * @param {string} name - Animation name
   * @param {boolean} restart - Restart if already playing this animation
   */
  play(name, restart = false) {
    const anim = this.animations.get(name);
    if (!anim) {
      console.warn(`Animation "${name}" not found`);
      return;
    }
    
    if (this.currentName === name && !restart) {
      return; // Already playing
    }
    
    this.current = anim;
    this.currentName = name;
    anim.reset();
  }
  
  /**
   * Update current animation
   * @param {number} dt - Delta time
   */
  update(dt) {
    if (this.current) {
      this.current.update(dt);
    }
  }
  
  /**
   * Get current frame from active animation
   * @returns {*} Current frame data
   */
  currentFrame() {
    return this.current ? this.current.current() : null;
  }
  
  /**
   * Get currently playing animation name
   * @returns {string|null}
   */
  getCurrentName() {
    return this.currentName;
  }
  
  /**
   * Check if current animation finished (for non-looping anims)
   * @returns {boolean}
   */
  isFinished() {
    return this.current ? this.current.isFinished() : false;
  }
}

/**
 * Sprite Sheet Helper
 * Slices a sprite sheet into frames
 * 
 * Usage:
 *   const sheet = new SpriteSheet(image, 32, 32); // 32x32 tiles
 *   const walkFrames = sheet.getFrames(0, 0, 4); // 4 frames starting at (0,0)
 *   const idleFrames = sheet.getFrames(0, 1, 2); // 2 frames from row 1
 */
class SpriteSheet {
  /**
   * @param {HTMLImageElement} image - Sprite sheet image
   * @param {number} frameWidth - Width of each frame
   * @param {number} frameHeight - Height of each frame
   * @param {number} margin - Margin between frames (optional)
   * @param {number} spacing - Spacing between frames (optional)
   */
  constructor(image, frameWidth, frameHeight, margin = 0, spacing = 0) {
    this.image = image;
    this.frameWidth = frameWidth;
    this.frameHeight = frameHeight;
    this.margin = margin;
    this.spacing = spacing;
    
    this.cols = Math.floor((image.width - margin) / (frameWidth + spacing));
    this.rows = Math.floor((image.height - margin) / (frameHeight + spacing));
  }
  
  /**
   * Get frame data at specific tile coordinates
   * @param {number} col - Column index
   * @param {number} row - Row index
   * @returns {Object} {x, y, w, h, img}
   */
  getFrame(col, row) {
    return {
      x: this.margin + col * (this.frameWidth + this.spacing),
      y: this.margin + row * (this.frameHeight + this.spacing),
      w: this.frameWidth,
      h: this.frameHeight,
      img: this.image
    };
  }
  
  /**
   * Get multiple frames in a row
   * @param {number} startCol - Starting column
   * @param {number} row - Row index
   * @param {number} count - Number of frames
   * @returns {Array} Array of frame objects
   */
  getFrames(startCol, row, count) {
    const frames = [];
    for (let i = 0; i < count; i++) {
      frames.push(this.getFrame(startCol + i, row));
    }
    return frames;
  }
  
  /**
   * Get all frames from the sheet
   * @returns {Array} Array of all frame objects
   */
  getAllFrames() {
    const frames = [];
    for (let row = 0; row < this.rows; row++) {
      for (let col = 0; col < this.cols; col++) {
        frames.push(this.getFrame(col, row));
      }
    }
    return frames;
  }
}

/**
 * Example: Complete Animation Setup
 * 
 * // Load sprite sheet
 * const spriteImg = new Image();
 * spriteImg.src = 'player.png';
 * 
 * spriteImg.onload = () => {
 *   const sheet = new SpriteSheet(spriteImg, 32, 32);
 *   
 *   // Create animations
 *   const controller = new AnimationController();
 *   controller.add('idle', new Animator(sheet.getFrames(0, 0, 4), 6));
 *   controller.add('run', new Animator(sheet.getFrames(0, 1, 8), 12));
 *   controller.add('jump', new Animator(sheet.getFrames(0, 2, 1), 1, false));
 *   
 *   // Play idle by default
 *   controller.play('idle');
 *   
 *   // In game loop:
 *   function update(dt) {
 *     // Update based on player state
 *     if (player.jumping) {
 *       controller.play('jump');
 *     } else if (player.moving) {
 *       controller.play('run');
 *     } else {
 *       controller.play('idle');
 *     }
 *     
 *     controller.update(dt);
 *   }
 *   
 *   function render(ctx) {
 *     const frame = controller.currentFrame();
 *     ctx.drawImage(
 *       frame.img,
 *       frame.x, frame.y, frame.w, frame.h,
 *       player.x, player.y, frame.w, frame.h
 *     );
 *   }
 * };
 */
