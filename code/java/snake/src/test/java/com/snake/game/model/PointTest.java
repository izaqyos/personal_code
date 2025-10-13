package com.snake.game.model;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PointTest {
    
    @Test
    void testPointCreation() {
        Point point = new Point(5, 10);
        assertEquals(5, point.getX());
        assertEquals(10, point.getY());
    }
    
    @Test
    void testPointEquality() {
        Point p1 = new Point(1, 2);
        Point p2 = new Point(1, 2);
        Point p3 = new Point(2, 1);
        
        assertEquals(p1, p2);
        assertNotEquals(p1, p3);
    }
    
    @Test
    void testHashCode() {
        Point p1 = new Point(1, 2);
        Point p2 = new Point(1, 2);
        
        assertEquals(p1.hashCode(), p2.hashCode());
    }
} 