// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package eu.stamp.camp.samples.testman.domain;

import eu.stamp.camp.samples.testman.domain.TCExecStatus;
import eu.stamp.camp.samples.testman.domain.TCExecution;
import eu.stamp.camp.samples.testman.domain.TCExecutionDataOnDemand;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import javax.validation.ConstraintViolation;
import javax.validation.ConstraintViolationException;
import org.springframework.stereotype.Component;

privileged aspect TCExecutionDataOnDemand_Roo_DataOnDemand {
    
    declare @type: TCExecutionDataOnDemand: @Component;
    
    private Random TCExecutionDataOnDemand.rnd = new SecureRandom();
    
    private List<TCExecution> TCExecutionDataOnDemand.data;
    
    public TCExecution TCExecutionDataOnDemand.getNewTransientTCExecution(int index) {
        TCExecution obj = new TCExecution();
        setExecutedOn(obj, index);
        setExecutionStatus(obj, index);
        setTester(obj, index);
        return obj;
    }
    
    public void TCExecutionDataOnDemand.setExecutedOn(TCExecution obj, int index) {
        Date executedOn = new GregorianCalendar(Calendar.getInstance().get(Calendar.YEAR), Calendar.getInstance().get(Calendar.MONTH), Calendar.getInstance().get(Calendar.DAY_OF_MONTH), Calendar.getInstance().get(Calendar.HOUR_OF_DAY), Calendar.getInstance().get(Calendar.MINUTE), Calendar.getInstance().get(Calendar.SECOND) + new Double(Math.random() * 1000).intValue()).getTime();
        obj.setExecutedOn(executedOn);
    }
    
    public void TCExecutionDataOnDemand.setExecutionStatus(TCExecution obj, int index) {
        TCExecStatus executionStatus = TCExecStatus.class.getEnumConstants()[0];
        obj.setExecutionStatus(executionStatus);
    }
    
    public void TCExecutionDataOnDemand.setTester(TCExecution obj, int index) {
        String tester = "tester_" + index;
        obj.setTester(tester);
    }
    
    public TCExecution TCExecutionDataOnDemand.getSpecificTCExecution(int index) {
        init();
        if (index < 0) {
            index = 0;
        }
        if (index > (data.size() - 1)) {
            index = data.size() - 1;
        }
        TCExecution obj = data.get(index);
        Long id = obj.getId();
        return TCExecution.findTCExecution(id);
    }
    
    public TCExecution TCExecutionDataOnDemand.getRandomTCExecution() {
        init();
        TCExecution obj = data.get(rnd.nextInt(data.size()));
        Long id = obj.getId();
        return TCExecution.findTCExecution(id);
    }
    
    public boolean TCExecutionDataOnDemand.modifyTCExecution(TCExecution obj) {
        return false;
    }
    
    public void TCExecutionDataOnDemand.init() {
        int from = 0;
        int to = 10;
        data = TCExecution.findTCExecutionEntries(from, to);
        if (data == null) {
            throw new IllegalStateException("Find entries implementation for 'TCExecution' illegally returned null");
        }
        if (!data.isEmpty()) {
            return;
        }
        
        data = new ArrayList<TCExecution>();
        for (int i = 0; i < 10; i++) {
            TCExecution obj = getNewTransientTCExecution(i);
            try {
                obj.persist();
            } catch (final ConstraintViolationException e) {
                final StringBuilder msg = new StringBuilder();
                for (Iterator<ConstraintViolation<?>> iter = e.getConstraintViolations().iterator(); iter.hasNext();) {
                    final ConstraintViolation<?> cv = iter.next();
                    msg.append("[").append(cv.getRootBean().getClass().getName()).append(".").append(cv.getPropertyPath()).append(": ").append(cv.getMessage()).append(" (invalid value = ").append(cv.getInvalidValue()).append(")").append("]");
                }
                throw new IllegalStateException(msg.toString(), e);
            }
            obj.flush();
            data.add(obj);
        }
    }
    
}
