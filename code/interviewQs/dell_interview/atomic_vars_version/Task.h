#ifndef __TASK__
#define __TASK__

#include <string>

class BaseTask
{

        public:
            virtual void execute() const = 0;
            const std::string& toString() const {return m_sName; }; 

        protected:
            std::string m_sName;
            friend std::ostream& operator<<(std::ostream & inpOS, const BaseTask & sched);
};

class Task1 : public BaseTask
{

        public:
                Task1(std::string  name);
                void execute() const;
};


class Task2 : public BaseTask
{
        public:
                Task2(std::string  name);
                void execute() const;
};

class Task3 : public BaseTask
{
        public:
                Task3(std::string  name);
                void execute() const;
};

#endif
