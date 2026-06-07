"""Command-line interface for digital clock with timezone support"""

import pytz
from datetime import datetime
import sys
import time
from pathlib import Path
import json

class MultiTimezoneClock:
    """Multi-timezone clock for terminal display"""
    
    def __init__(self, timezones=None):
        """Initialize clock with timezones"""
        self.timezones = timezones or ['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo']
    
    def add_timezone(self, tz):
        """Add a timezone"""
        if tz not in self.timezones:
            self.timezones.append(tz)
    
    def remove_timezone(self, tz):
        """Remove a timezone"""
        if tz in self.timezones:
            self.timezones.remove(tz)
    
    def get_time(self, tz_name):
        """Get current time in timezone"""
        try:
            tz = pytz.timezone(tz_name)
            return datetime.now(tz)
        except Exception as e:
            return None
    
    def get_all_times(self):
        """Get current times in all timezones"""
        times = {}
        for tz_name in self.timezones:
            current_time = self.get_time(tz_name)
            if current_time:
                times[tz_name] = current_time
        return times
    
    def display(self, format_24h=False):
        """Display clock in terminal"""
        times = self.get_all_times()
        
        # Clear screen
        sys.stdout.write('\033[2J\033[H')
        
        print("\n" + "="*70)
        print(" " * 15 + "DIGITAL CLOCK - MULTI-TIMEZONE")
        print("="*70 + "\n")
        
        for tz_name in self.timezones:
            if tz_name in times:
                current_time = times[tz_name]
                if format_24h:
                    time_str = current_time.strftime('%H:%M:%S')
                else:
                    time_str = current_time.strftime('%I:%M:%S %p')
                
                date_str = current_time.strftime('%A, %B %d, %Y')
                offset = current_time.strftime('%z')
                offset_formatted = f"UTC{offset[:3]}:{offset[3:]}"
                
                print(f"  {tz_name:25} | {time_str:12} | {offset_formatted:8}")
                print(f"  {'':25} | {date_str}")
                print()
        
        print("="*70)
        print(f"  Format: {'24-hour' if format_24h else '12-hour'} | Press Ctrl+C to exit")
        print("="*70 + "\n")

def main():
    """Main CLI function"""
    clock = MultiTimezoneClock()
    
    print("\n=== Digital Clock with Timezone Support ===")
    print("\n1. Display clock")
    print("2. Add timezone")
    print("3. Remove timezone")
    print("4. Show all timezones")
    print("5. Exit\n")
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                format_24h = input("Use 24-hour format? (y/n): ").lower() == 'y'
                print("\nPress Ctrl+C to stop...\n")
                try:
                    while True:
                        clock.display(format_24h)
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n\nStopped.\n")
            
            elif choice == '2':
                print(f"\nCurrent timezones: {', '.join(clock.timezones)}")
                print("Available timezones: ", end="")
                tz_input = input("Enter timezone to add: ").strip()
                try:
                    pytz.timezone(tz_input)
                    clock.add_timezone(tz_input)
                    print(f"Added {tz_input}\n")
                except:
                    print(f"Invalid timezone: {tz_input}\n")
            
            elif choice == '3':
                print(f"\nCurrent timezones: {', '.join(clock.timezones)}")
                tz_input = input("Enter timezone to remove: ").strip()
                clock.remove_timezone(tz_input)
                print(f"Removed {tz_input}\n")
            
            elif choice == '4':
                print(f"\nConfigured timezones: {', '.join(clock.timezones)}\n")
            
            elif choice == '5':
                print("\nExiting...\n")
                break
            
            else:
                print("Invalid choice. Please try again.\n")
        
        except KeyboardInterrupt:
            print("\n\nExiting...\n")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == '__main__':
    main()
